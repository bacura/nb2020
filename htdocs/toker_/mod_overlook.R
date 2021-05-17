## R script for TokeR module for overlook 0.00b

#### mod設定
mod <- 'overlook'

#### おまじない
Sys.timezone( location = TRUE )

#### MariaDBライブラリの呼び出し
library( RMariaDB )

#### コマンドラインの第一引数からトークンを受け取る
token = commandArgs( trailingOnly = TRUE )[1]

#### コマンドラインの第二引数をからDBユーザー名を受け取る
user = commandArgs( trailingOnly = TRUE )[2]

#### S4 method を使ってDBに接続する
con <- dbConnect( RMariaDB::MariaDB(), dbname = "rr2020", username = user )


################################################################################################

#### サンプルデータを抽出するクエリを作成する
query <- paste( "SELECT data FROM ", mod, " WHERE token='", token ,"';", sep = "" )

#### クエリをDBに送り、結果を受けとる。
res <- dbSendQuery( con, query )

#### 結果から塊データを受け取る
solid <- dbFetch( res,  row.names = FALSE )

#### 塊データをタブ区切りのベクトルにする
c <- strsplit( solid[1,1], "\t" )[[1]]

#### タブ区切りは文字なので数値データに変換する
nc <- as.numeric( c )

#### 数値データはベクトル型をフレームデータ型の変換する（カラム名はSAMPLE)
data <- data.frame( SAMPLE=nc )

#### 結果をクリアする
dbClearResult( res )


#################################################################################################

#### データフレームのTEST行の平均値を計算し、SQLを作成
mean_r <- mean( data$SAMPLE )
mean_s <- paste( " mean='", mean_r, "',", sep = "" )

#### データフレームのTEST行の中央値を計算SQLを作成
median_r <- median( data$TEST )
median_s <- paste( " median='", median_r, "'", sep = "" )


#################################################################################################

#### 結果をDBに格納するクリエを作成する
query <- paste( "UPDATE ", mod, " set", mean_s, median_s, " WHERE token='", token ,"';", sep = "" )

#### クエリをDBに送り、結果を受けとる
res <- dbSendQuery( con, query )

#### 結果をクリアする
dbClearResult( res )


#################################################################################################

#### DBサーバーとの接続を切る。
dbDisconnect( con )
