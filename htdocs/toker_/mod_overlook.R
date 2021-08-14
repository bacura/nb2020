## R script for TokeR module for overlook 0.00b


#### 作業ディレクトリの設定
setwd( "/tmp" )

#### MariaDBライブラリの呼び出し
library( RMariaDB )
library( ggplot2)

#### コマンドラインの第１引数からトークンを受け取る
mod <- commandArgs( trailingOnly = TRUE )[1]
mod

#### コマンドラインの第２引数からトークンを受け取る
token <- commandArgs( trailingOnly = TRUE )[2]
token

#### コマンドラインの第３引数からDB名を受け取る
db <- commandArgs( trailingOnly = TRUE )[3]
db

#### コマンドラインの第４引数からDBユーザー名を受け取る
user <- commandArgs( trailingOnly = TRUE )[4]
user

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

#### 数値データはベクトル型をフレームデータ型の変換する（カラム名はSAMPLE)
data <- data.frame( SAMPLE=nc )

#### 結果をクリアする
dbClearResult( res )


#################################################################################################

#### データフレームのSAMPLE行のサンプル数をカウントし、SQLを作成
num_r <- length( data$SAMPLE )
num_s <- paste( " num_='", num_r, "',", sep = "" )

### データフレームのSAMPLE行の合計値を計算し、SQLを作成
sum_r <- sum( data$SAMPLE )
sum_s <- paste( " sum_='", sum_r, "',", sep = "" )

### データフレームのSAMPLE行の平均値を計算し、SQLを作成
mean_r <- mean( data$SAMPLE )
mean_s <- paste( " mean_='", mean_r, "',", sep = "" )

#### データフレームのSAMPLE行の最小値を計算し、SQLを作成
min_r <- min( data$SAMPLE )
min_s <- paste( " min_='", min_r, "',", sep = "" )

#### データフレームのSAMPLE行の最大値を計算し、SQLを作成
max_r <- max( data$SAMPLE )
max_s <- paste( " max_='", max_r, "',", sep = "" )

#### データフレームのSAMPLE行の中央値を計算SQLを作成
median_r <- median( data$SAMPLE )
median_s <- paste( " median_='", median_r, "',", sep = "" )

#### データフレームのSAMPLE行の分散値を計算SQLを作成
var_r <- var( data$SAMPLE ) * ( length( data$SAMPLE ) - 1 ) / length( data$SAMPLE )
var_s <- paste( " var_='", var_r, "',", sep = "" )

#### データフレームのSAMPLE行の標準偏差値を計算SQLを作成
sd_r <- sqrt( var_r )
sd_s <- paste( " sd_='", sd_r, "'", sep = "" )


#################################################################################################

#### 一時ファイルの名前を合成
tmp_file <- paste( token, ".png", sep = "" )
tmp_file

#### 新しい描画デバイスを開き、マージンを調節する。
#dev.new()
par( 'mar' = c( 1, 1, 1, 1 ))

#### PNG形式のパラメーターを設定する。
png( tmp_file, width = 1000, height = 1000, units = 'px', pointsize = 16, bg = 'white', type="cairo" )

#### ggplot2でヒストグラムを描画
g <- ggplot( data, aes( x = SAMPLE ))
g <- g + geom_histogram()
plot( g )

#### グラフを書いて、描画デバイスを閉じる
dev.off()


#################################################################################################

#### 一時ファイルの名前を合成
tmp_file <- paste( token, ".pdf", sep = "" )
tmp_file

#### 新しい描画デバイスを開き、マージンを調節する。
#dev.new()
par( 'mar' = c( 1, 1, 1, 1 ))

#### PDF形式のパラメーターを設定する。
cairo_pdf( tmp_file )

#### グラフを書く
# プロットは同じなので省略
plot( g )


#### 描画デバイスを閉じる
dev.off()

#################################################################################################

#### 結果をDBに格納するクリエを作成する
query <- paste( "UPDATE ", mod, " set", num_s, sum_s, mean_s, median_s, min_s, max_s, var_s, sd_s, " WHERE token='", token ,"';", sep = "" )
query

#### クエリをDBに送り、結果を受けとる
res <- dbSendQuery( con, query )

#### 結果をクリアする
dbClearResult( res )


#################################################################################################

#### DBサーバーとの接続を切る。
dbDisconnect( con )
