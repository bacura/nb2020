#! /usr/bin/ruby
# coding: utf-8
#Nutrition browser 2020 login 0.06b (2023/07/15)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
  l = Hash.new

  #Japanese
  l['jp'] = {
    'message'   => "IDとパスワードを入力してログインしてください。",\
    'password'  => "パスワード",\
    'login'   => "ログイン",\
    'error'   => "IDとパスワードが一致しませんでした。<br>パスワードを忘れた方は再登録してください。",\
    'help'  => "<img src='bootstrap-dist/icons/question-circle-ndsk.svg' style='height:3em; width:2em;'>",\
    'nb'    => "栄養ブラウザ",\
    'regist'  => "登録",\
    'empty'   => "[空き地]"
  }

  return l[language]
end


#### HTML login
def html_login_form( msg, l )
  html = <<-"HTML"
    <div class="container">
      <div class="row">
        <div class="col-6">
          <form action="login.cgi?mode=check" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{l['message']}</p>
          <input type="text" name="id" id="inputID" class="form-control login_input" placeholder="ID" required autofocus>
          <input type="password" name="pass" id="inputPassword" class="form-control login_input" placeholder="#{l['password']}">
          <input type="submit" value="#{l['login']}" class="btn btn-primary btn-block"></input>
          </form>
        </div>
        <div class="col-6">
          #{l['empty']}
        </div>
      </div>
    </div>
HTML

  puts html
end


#### HTML top
def html_top_login( l )
  login_color = "secondary"
  login = "<a href=\"regist.cgi\" class=\"text-#{login_color}\">#{l['regist']}</a>"

  html = <<-"HTML"
<header class="navbar navbar-expand-lg navbar-dark bg-dark" id="header">
  <div class="container-fluid">
    <a href="index.cgi" class="navbar-brand h1 text-#{login_color}">#{l['nb']}</a>
    <span class="navbar-text text-#{login_color} login_msg h4">#{login}</span>
    <a href='https://bacura.jp/?page_id=543' target='manual'>#{l['help']}</a>
  </div>
</header>
HTML

  puts html
end

#==============================================================================
# Main
#==============================================================================
text_init() if @debug

#### Getting GET data
get_data = get_data()

#### Getting POST date
user = User.new( @cgi )
l = language_pack( user.language )
db = Db.new( user, false, true )

puts "#{get_data['mode']}" if @debug
case get_data['mode']
when 'check'

  puts 'Checking user ID on DB' if @debug
  r = db.query( "SELECT user, status, cookie FROM #{$MYSQL_TB_USER} WHERE user='#{@cgi['id']}' AND pass='#{@cgi['pass']}' AND status>'0';", false )
  unless r.first
      html_init( nil )
      html_head( nil, 0, nil )
      html_top_login( l )
      msg = "<p class='msg_small_red'>#{l['error']}</p>"
      html_login_form( msg, l )
      html_foot()
  else
    status = r.first['status'].to_i

    puts 'Issuing cookies' if @debug
    uid = SecureRandom.hex( 16 )
    uid = r.first['cookie'] if status == 7 && r.first['cookie'] != nil
    cookie = "Set-Cookie: NAME=#{@cgi['id']}\nSet-Cookie: #{$COOKIE_UID}=#{uid}\n"

    puts 'Updating user information' if @debug
    db.query( "UPDATE #{$MYSQL_TB_USER} SET cookie='#{uid}', cookie_m=NULL WHERE user='#{@cgi['id']}';", true )

    html_init( cookie )
    html_head( 'refresh', status, nil )
    puts '</span></body></html>'

    puts 'Init essential config' if @debug
    if status != 7
      # Checking & repairing history table
      r = db.query( "SELECT user FROM #{$MYSQL_TB_HIS} WHERE user='#{@cgi['id']}';", false )
      db.query( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{@cgi['id']}', his='';", true )  unless r.first

      # Checking & repairing SUM table
      r = db.query( "SELECT user FROM #{$MYSQL_TB_SUM} WHERE user='#{@cgi['id']}';", false )
      db.query( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{@cgi['id']}', sum='';", true ) unless r.first

      # Checking & repairing meal table
      r = db.query( "SELECT user FROM #{$MYSQL_TB_MEAL} WHERE user='#{@cgi['id']}';", false )
      db.query( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{@cgi['id']}', meal='';", true ) unless r.first
    end
  end

when 'logout'
  # Meaningless Cookie
  cookie = "Set-Cookie: NAME=NULL\nSet-Cookie: #{$COOKIE_UID}=NULL\n"
  html_init( cookie )
  html_head( 'refresh', 0, nil )
  puts '</span></body></html>'
  db.query( "UPDATE #{$MYSQL_TB_USER} SET cookie_m=NULL WHERE user='#{user.name}';", true )

when 'family'
  cookie = ''
  login_mv = get_data['login_mv']
  puts "->#{login_mv}" if @debug
  r = db.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{login_mv}';", false )
  if r.first
    puts r.first['mom'] if @debug
    if r.first['mom'] == '' ||  r.first['mom'] == nil
        cookie = "Set-Cookie: NAME=#{login_mv}\nSet-Cookie: #{$COOKIE_UID}=#{r.first['cookie']}\n"
        db.query( "UPDATE #{$MYSQL_TB_USER} SET cookie_m=NULL WHERE user='#{user.name}';", true )
    else
      rr = db.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user=\"#{r.first['mom']}\";", false )
      if rr.first
        # Issuing cookies
        uid = SecureRandom.hex( 16 )
        mid = rr.first['cookie']
        cookie = "Set-Cookie: NAME=#{login_mv}\nSet-Cookie: #{$COOKIE_UID}=#{uid}\n"
        puts cookie if @debug

        db.query( "UPDATE #{$MYSQL_TB_USER} SET cookie='#{uid}', cookie_m='#{mid}' WHERE user='#{login_mv}';", true )
        db.query( "UPDATE #{$MYSQL_TB_USER} SET cookie_m=NULL WHERE user='#{user.name}';", true )
      end
    end
  end
  html_init( cookie )

  html_head( 'refresh', r.first['status'], nil )
  puts '</span></body></html>'

# Input form init
else
  html_init( nil )
  html_head( nil, 0, nil )
  html_top_login( l )
  html_login_form( nil, l )
  html_foot()
end
