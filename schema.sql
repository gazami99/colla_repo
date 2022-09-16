 USE test;

DROP TABLE IF EXISTS covid_info;
    
CREATE TABLE covid_info
(            
   info_no int auto_increment,
   conf_case int,
   conf_caserate int,
   create_dt varchar(20),
   critical_rate int,
   death int,
   death_rate int,
   gubun varchar(20),
   CONSTRAINT pk_covidinfo PRIMARY KEY ( info_no )
);

