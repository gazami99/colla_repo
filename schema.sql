 USE test;

DROP TABLE IF EXISTS covidinfo;
    
CREATE TABLE covidinfo
(            
   infoNo int auto_increment,
   confcase int,
   confcaseRate int,
   creaeDt varchar(20),
   criticalRate int,
   death int,
   deateRate int,
   gubun varchar(20),
   CONSTRAINT pk_covidinfo PRIMARY KEY ( infoNo )
);

