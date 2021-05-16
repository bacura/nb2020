## test.R


#### MariaDBライブラリの呼び出し
library( RMariaDB )


#### MariaDBからデータを受け取り
# コマンドラインの第一引数をトークンとする
token = commandArgs( trailingOnly = TRUE )[1]

# S4 method を使ってMariaDBサーバーに接続する。
con <- dbConnect( RMariaDB::MariaDB(), dbname = "rr2020", username = "userr" )

# クエリを設定する
query <- paste( "SELECT data FROM test WHERE token='", token ,"';", sep = "" )

# クエリをサーバーに送り、結果を受けとる。
res <- dbSendQuery( con, query )

# 結果から塊データを受け取る
solid <- dbFetch( res,  row.names = FALSE )

# 塊データをタブ区切りのベクトルにする
c <- strsplit( solid[1,1], "\t" )[[1]]

# 数値データに変換
nc <- as.numeric( c )

# フレームデータの変換する
data <- data.frame( TEST=nc )

# 結果をクリアする
dbClearResult( res )


#### データを統計処理
# TEST行の値の平均値を計算
result <- mean( data$TEST )


#### MariaDBにデータを受け渡し
# クリエを設定する
query <- paste( "UPDATE test set result='", result, "' WHERE token='", token ,"';", sep = "" )

# クエリをサーバーに送り、結果を受けとる。
res <- dbSendQuery( con, query )

#### 結果をクリアする
dbClearResult( res )


#### MariaDBサーバーとの接続を切る。
dbDisconnect( con )
