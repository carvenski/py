package cdc;

import java.util.UUID;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class CDC_ci_infra {

    public static void main(String[] args) throws Exception {

        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // must open checkpoint, Flink Doris Connector write data by it
        env.enableCheckpointing(10*1000);

        env.setParallelism(1);
      
        final StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);
        
        String jobName = "CDC_ci_infra";
        tEnv.getConfig().getConfiguration().setString("pipeline.name", jobName);
        
        // =========================================================
        // FUCK
        // 之前一直报错用户mysql表中的time字段和flink sql time关键字冲突了
        // 搞了三天时间查询了所有google都没答案
        // 加了三天班没办法用不了sql 只能用java datastream api重写sql任务
        // 今天早上不知怎么突然想起来在字段前面加个 `time` 括起来 试了一下
        // 就好了。。。日
        // `time` INT
        // 注: sql中使用 `` 来区分保留关键字和用户字段 (don't konw that)
        // =========================================================

        // register a table in the catalog
        tEnv.executeSql(
            "CREATE TABLE SS (\n" +
                "  id INT,\n" +
                "  service_name STRING,\n" +
                "  `time` INT,\n" +
                "  flag INT,\n" +                
                "  PRIMARY KEY(id) NOT ENFORCED\n" +
                ") WITH (\n" +
                "  'connector' = 'mysql-cdc',\n" +
                "  'hostname' = '',\n" +
                "  'port' = '',\n" +
                "  'username' = '',\n" +
                "  'password' = '',\n" +
                "  'database-name' = 'ci_infra_dashboard',\n" +
                "  'table-name' = 'ci_infra',\n" +
                "  'scan.startup.mode' = 'latest-offset'\n" +
                ")");
        
        //doris table
        tEnv.executeSql(
            "CREATE TABLE DD (\n" +
                "  id INT,\n" +
                "  service_name STRING,\n" +
                "  time_ INT,\n" +
                "  flag INT\n" +    
                ") \n" +
                "WITH (\n" +
                "  'connector' = 'doris',\n" +
                "  'fenodes' = 'ip:18030',\n" +
                "  'table.identifier' = 'test.ci_infra',\n" +
                "  'username' = '',\n" +
                "  'password' = '',\n" +    
                "  'sink.label-prefix' = 'doris_label_" + UUID.randomUUID().toString() + "',\n" +               
                "  'sink.enable-delete' = 'true',\n" +
                "  'sink.properties.format' = 'json',\n" +  
                "  'sink.properties.read_json_by_line' = 'true'\n" +
                ")");

        //insert into mysql table to doris table
        tEnv.executeSql("INSERT INTO DD select * from SS");
    }
}
