doas ## test.R


#### library
library( RMariaDB )


#### Get token
token = commandArgs( trailingOnly = TRUE )[1]


#### S4 method for signature 'MariaDBDriver'
con <- dbConnect( RMariaDB::MariaDB(), dbname = "rr2020", username = "rru" )


#### Get data from DB & modify
query <- paste( "SELECT data FROM test WHERE token='", token ,"';", sep = "" )
res <- dbSendQuery( con, query )
solid <- dbFetch( res,  row.names = FALSE )
c <- strsplit( solid[1,1], "\t" )[[1]]
nc <- as.numeric( c )
data <- data.frame( TEST=nc )
dbClearResult( res )


#### Process data
result <- mean( data$TEST )


#### Update DB to weite a result
query <- paste( "UPDATE test set result='", result, "' WHERE token='", token ,"';", sep = "" )
res <- dbSendQuery( con, query )
dbClearResult( res )


#### Cean up
dbDisconnect( con )
