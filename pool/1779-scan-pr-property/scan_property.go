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
	fmt.Println("[start] scan property table")
	// *************************************************************************
	// var q chan *[1000][2]string = make(chan *[1000][2]string, 9)
	// *************************************************************************
	var q chan *[1000][2]string = make(chan *[1000][2]string, 1000)
	// var username, password, addrs, database = "movoto", "movoto123!", "db3.ng.movoto.net", "movoto"
	var username, password, addrs, database = "wentao-ro", "admin@123", "10.255.1.6", "movoto"
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
	go scan_property(db, q, &wg)
	wg.Add(1)
	// *************************************************************************
	//for i := 0; i < 9; i++ {
	// *************************************************************************
	for i := 0; i < 1000; i++ {
		go check_property(db, q, &wg)
		wg.Add(1)
	}
	wg.Wait() // time.Sleep(time.Second * 3600 * 10)
	fmt.Println("====task done==== All go routines finished executing")
}

func scan_property(db *sql.DB, q chan *[1000][2]string, wg *sync.WaitGroup) {
	start_id := ""
	t := 0
	for {
		fmt.Println("[scaning] from property id: ", start_id)
		_sql := "SELECT mp.id, mp.public_record_id FROM mls_public_record_association AS mp WHERE mp.id>? ORDER BY mp.id ASC LIMIT 1000;"
		rows, err := db.Query(_sql, start_id)
		if err != nil {
			fmt.Println(err)
			panic(err.Error())
		}
		defer rows.Close()
		//-------------------------
		var _id sql.NullString
		var _p_pr_id sql.NullString
		var id string
		var p_pr_id string
		// ------------------------
		var l [1000][2]string
		i := 0
		for rows.Next() {
			err = rows.Scan(&_id, &_p_pr_id)
			if _id.Valid {
				id = _id.String
			} else {
				id = ""
			}
			if _p_pr_id.Valid {
				p_pr_id = _p_pr_id.String
			} else {
				p_pr_id = ""
			}
			if err != nil {
				fmt.Println(err)
				panic(err.Error())
			}
			l[i][0] = id      // p_id
			l[i][1] = p_pr_id // p_pr_id
			i += 1
			start_id = id
		}
		// start_id = id // it's ok here ?
		t += i
		fmt.Println("                                                total => ", t)
		if l[0][0] == "" { //l[0][0] is p_id, "" means end of property table
			fmt.Println("[done] scan property done")
			// *************************************************************************
			// for i := 0; i < 9; i++ { //number = 9 check_property, to send exit signal
			// *************************************************************************
			for i := 0; i < 1000; i++ { //number = 1000 check_property, to send exit signal
				q <- &l
			}
			wg.Done()
			break
		}
		q <- &l
	}
}

func check_property(db *sql.DB, q chan *[1000][2]string, wg *sync.WaitGroup) {
	var c chan bool = make(chan bool)
	for {
		l := *(<-q)
		if l[0][0] == "" { //l[0][0] is p_id, "" means scan is over and queue is empty
			fmt.Println("[exit] of 1 check_property")
			wg.Done()
			break
		}
		fmt.Println("[checking] 1000 property")
		for _, i := range l {
			p_id := i[0]
			p_pr_id := i[1]
			if p_pr_id == "" { // skip p_pr_id is empty
				continue
			}
			if p_id == "" { // last batch may be: 0 < length < 1000, cause l is array which length=1000.
				break
			}
			go find_p_pr_exists_or_point_other(p_pr_id, p_id, db, c)
			<-c //need to block here to make sure this goroutine already finish
		}
	}
}

func find_p_pr_exists_or_point_other(pr_id string, pA_id string, db *sql.DB, c chan bool) {
	_sql := "SELECT id, property_id FROM public_record AS pr WHERE pr.id=?;"
	rows, err := db.Query(_sql, pr_id)
	if err != nil {
		fmt.Println(err)
		panic(err.Error())
	}
	defer rows.Close()
	var _pB_id sql.NullString // _pB_id may be empty
	var id string             // id may be empty too but if id empty, won't into loop
	var pB_id string
	var c2 chan bool = make(chan bool)
	for rows.Next() { // if id not exists, won't into this loop
		err = rows.Scan(&id, &_pB_id)
		if err != nil {
			fmt.Println(err)
			panic(err.Error())
		}
		if _pB_id.Valid {
			pB_id = _pB_id.String
		} else {
			pB_id = ""
		}
		if id == "" {
			// 4.property's pr_id not exist in pr table
			fmt.Println("[find] property's pr_id not exist, p_id: ", pA_id)
			go find_pr_by_p_address(pA_id, db, c2)
			<-c2 //need to block here to make sure this goroutine already finish
		} else {
			// 5.p-A has pr has p-B
			if pB_id != "" && pB_id != pA_id {
				fmt.Println("[find] p-A has pr has p-B ", pA_id, id, pB_id)
			}
		}
	}
	c <- false
}

func find_pr_by_p_address(p_id string, db *sql.DB, c chan bool) {
	_sql := `SELECT pr.id FROM mls_public_record_association AS mp 
             INNER JOIN address AS ad1 ON mp.address_id=ad1.id 
             INNER JOIN address AS ad2 ON ad1.address=ad2.address
             INNER JOIN public_record AS pr ON pr.address_id=ad2.id
             WHERE mp.id=?
             ORDER BY pr.update_time DESC 
             LIMIT 1 ;
             `
	rows, err := db.Query(_sql, p_id)
	if err != nil {
		fmt.Println(err)
		panic(err.Error())
	}
	defer rows.Close()
	var id string
	for rows.Next() { // if into loop, then pr_id exists
		err = rows.Scan(&id)
		if err != nil {
			fmt.Println(err)
			panic(err.Error())
		}
		fmt.Println("[found] pr by p address: ", id)
	}
	c <- false
}
