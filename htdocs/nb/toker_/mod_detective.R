## R script for test module of TokeR 0.00b


#### 作業ディレクトリの設定
setwd( "/tmp" )

#### MariaDBライブラリの呼び出し
library( RMariaDB )

#### コマンドラインの第１引数からトークンを受け取る
mod <- commandArgs( trailingOnly = TRUE )[1]

#### コマンドラインの第２引数からトークンを受け取る
token <- commandArgs( trailingOnly = TRUE )[2]

#### コマンドラインの第３引数からDB名を受け取る
db <- commandArgs( trailingOnly = TRUE )[3]

#### コマンドラインの第４引数からDBユーザー名を受け取る
user <- commandArgs( trailingOnly = TRUE )[4]

#### S4 method を使ってDBに接続する
con <- dbConnect( RMariaDB::MariaDB(), dbname = db, username = user )


################################################################################################

#### サンプルデータを抽出するクエリを作成する
query <- paste( "SELECT data FROM ", mod, " WHERE token='", token ,"';", sep = "" )
query

#### クエリをDBに送り、結果を受けとる。
res <- dbSendQuery( con, query )

#### 結果から塊データを受け取る
solid <- dbFetch( res,  row.names = FALSE )

#### 塊データをタブ区切りのベクトルにする
c <- strsplit( solid[1,1], "\t" )[[1]]

#### タブ区切りは文字なので数値データに変換する
nc <- as.numeric( c )

#### 数値データはベクトル型をフレームデータ型の変換する（カラム名はSAMPLE）
data <- data.frame( SAMPLE=nc )

#### 結果をクリアする
dbClearResult( res )


#################################################################################################

#### データフレームのTEST行の平均値を計算し、SQLを作成
mean_r <- mean( data$SAMPLE )
mean_s <- paste( " result='", mean_r, "'", sep = "" )


#################################################################################################

#### 結果をDBに格納するクリエを作成する
query <- paste( "UPDATE ", mod, " set", mean_s, " WHERE token='", token ,"';", sep = "" )
query

#### クエリをDBに送り、結果を受けとる
res <- dbSendQuery( con, query )

#### 結果をクリアする
dbClearResult( res )


#################################################################################################

#### DBサーバーとの接続を切る
dbDisconnect( con )
