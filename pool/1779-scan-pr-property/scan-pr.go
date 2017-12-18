package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"sync"
	"time"
)

// reference: https://github.com/yxzoro/mydjango/tree/master/Project/pool
// *********************************************************************************************************************
//            only 10 connections in pool = 1 producer + 9 consumers
//            so, only 10 concurrency mysql querys at most at sametime, whatever how many coroutines you use...
//            even 1000 coroutines just equals to 9 per batch but many batches...the concurrency number is 9 actually...
//            but bigger queue may cause faster producer, so more goods in queue for consumer to consume...?
// *********************************************************************************************************************

func main() {
	fmt.Println("[start] scan pr table")
	// *************************************************************************
	// var q chan *[1000][2]string = make(chan *[1000][2]string, 9)
	// *************************************************************************
	var q chan *[1000][2]string = make(chan *[1000][2]string, 1000)
	var username, password, addrs, database = "movoto", "movoto123!", "db3.ng.movoto.net", "movoto"
	params := fmt.Sprintf("%s:%s@tcp(%s)/%s?timeout=60s", username, password, addrs, database)
	db, err := sql.Open("mysql", params)  // db is a connection pool // db is pointer already
	db.SetMaxIdleConns(10)                // set connection num in pool, when this num bigger, db cpu bigger,
	db.SetMaxOpenConns(10)                //10 = 1 + 9              // mysql db cpu load: (10->40% 20->60% 40->70%)
	db.SetConnMaxLifetime(time.Hour * 10) // set one long connection max lifetime
	defer db.Close()
	if err != nil {
		fmt.Println(err)
		panic(err.Error())
	}
	var wg sync.WaitGroup
	go scan_pr(db, q, &wg)
	wg.Add(1)
	// *************************************************************************
	// for i := 0; i < 9; i++ {
	// *************************************************************************
	for i := 0; i < 1000; i++ {
		go check_pr(db, q, &wg)
		wg.Add(1)
	}
	wg.Wait() // time.Sleep(time.Second * 3600 * 10)
	fmt.Println("====task done==== All go routines finished executing")
}

func scan_pr(db *sql.DB, q chan *[1000][2]string, wg *sync.WaitGroup) {
	start_id := ""
	t := 0
	for {
		fmt.Println("[scaning] from pr id: ", start_id)
		_sql := "SELECT pr.id, pr.property_id FROM public_record AS pr WHERE pr.id>? ORDER BY pr.id ASC LIMIT 1000;"
		rows, err := db.Query(_sql, start_id)
		if err != nil {
			fmt.Println(err)
			panic(err.Error())
		}
		defer rows.Close()
		//----------------------
		var _id sql.NullString
		var _p_id sql.NullString // cause db may return nil, but string can't assign nil, so translate self
		var id string
		var p_id string
		// ---------------------
		var l [1000][2]string
		i := 0
		for rows.Next() { // if rows is empty, won't into this loop
			err = rows.Scan(&_id, &_p_id)
			if _id.Valid {
				id = _id.String
			} else {
				id = ""
			}
			if _p_id.Valid {
				p_id = _p_id.String
			} else {
				p_id = ""
			}
			if err != nil {
				fmt.Println(err)
				panic(err.Error())
			}
			l[i][0] = id   // pr_id
			l[i][1] = p_id // pr_p_id
			i += 1
			start_id = id
		}
		t += i
		fmt.Println("                                                total => ", t)
		if l[0][0] == "" { // l[0][0] is pr_id, "" means end of table pr
			fmt.Println("[done] scan pr done")
			// *************************************************************************
			// for i := 0; i < 9; i++ { //number = 9, to let 9 check_pr goroutine exit
			// *************************************************************************
			for i := 0; i < 1000; i++ { //number = 1000, to let 1000 check_pr goroutine exit
				q <- &l
			}
			wg.Done()
			break
		}
		q <- &l
	}
}

func check_pr(db *sql.DB, q chan *[1000][2]string, wg *sync.WaitGroup) {
	var c chan bool = make(chan bool)
	for {
		l := *(<-q)
		if l[0][0] == "" { // l[0][0] is pr_id, "" means scan is over and queue is empty
			fmt.Println("[exit] of 1 check_pr")
			wg.Done()
			break
		}
		fmt.Println("[checking] 1000 pr")
		for _, i := range l {
			pr_id := i[0]
			pr_p_id := i[1]
			if pr_id == "" { // last batch may be: 0 < length < 1000, cause l is array which length=1000.
				break
			}
			// 1.pr has no property
			if pr_p_id == "" {
				fmt.Println("[found] pr have no property: ", pr_id)
				continue
			}
			// 2.pr's property not exist in property table
			go find_if_p_exists(pr_p_id, pr_id, db, c)
			pr_p_exists := <-c //need to block here in logic to wait another goroutine's result
			if !pr_p_exists {
				continue
			}
			// 3.pr has multi property
			go find_pr_multi_p(pr_id, db, c)
			<-c //need to block here to make sure this goroutine already finish
		}
	}
}

func find_if_p_exists(pr_p_id string, pr_id string, db *sql.DB, c chan bool) {
	sql_to_find_if_p_exist := "SELECT id FROM mls_public_record_association AS mp WHERE mp.id=?;"
	rows, err := db.Query(sql_to_find_if_p_exist, pr_p_id)
	if err != nil {
		fmt.Println(err)
		panic(err.Error())
	}
	defer rows.Close()
	var p_id string
	for rows.Next() { // if p_id not exists, won't come into this loop at all, so p_id == ""
		err = rows.Scan(&p_id)
		if err != nil {
			fmt.Println(err)
			panic(err.Error())
		}
	}
	if p_id == "" {
		fmt.Println("[found] pr property not exists: ", pr_id)
		c <- false
	} else {
		c <- true
	}
}

func find_pr_multi_p(pr_id string, db *sql.DB, c chan bool) {
	sql_to_find_pr_multi_p := "SELECT id FROM mls_public_record_association AS mp WHERE mp.public_record_id=?;"
	rows, err := db.Query(sql_to_find_pr_multi_p, pr_id)
	if err != nil {
		fmt.Println(err)
		panic(err.Error())
	}
	defer rows.Close()
	var p_id string
	var p_id_list []string
	for rows.Next() { // definitely into this loop, at least 1
		err = rows.Scan(&p_id)
		if err != nil {
			fmt.Println(err)
			panic(err.Error())
		}
		p_id_list = append(p_id_list, p_id)
	}
	if len(p_id_list) > 1 {
		fmt.Println("[found] pr has multi property: ", pr_id)
	}
	c <- false
}
