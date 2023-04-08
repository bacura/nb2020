#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 regist 0.08b (2023/01/11)

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
    'nb'    => "栄養ブラウザ",\
    'login'   => "ログイン",\
    'help'    => "<img src='bootstrap-dist/icons/question-circle-ndsk.svg' style='height:2em; width:2em;'>",\
    'message'   => "IDとパスワードは必須です。英数字とアンダーバー(_)のみ使用可能です。ご登録前に利用規約を確認しておいてください。",\
    'id_rule'   => "ID (4~30文字)",\
    'pass_rule' => "パスワード (30文字まで)",\
    'a_rule'  => "二つ名 (60文字まで)",\
    'mail_rule' => "メールアドレス (60文字まで)",\
    'submit'  => "送信",\
    'error1'  => "入力されたIDは英数字とハイフン、アンダーバー以外の文字が使用されています。別のIDを入力して登録してください。",\
    'error2'  => "入力されたIDは制限の30文字を越えています。別のIDを入力して登録してください。",\
    'error3'  => "IDは4文字以上の長さが必要です。別のIDを入力して登録してください。",\
    'error4'  => "入力されたIDはすでに使用されています。別のIDを入力して登録してください。",\
    'confirm' => "下記の内容でよろしければ登録してください。",\
    'id'    => "ID",\
    'aliase'  => "二つ名",\
    'mail'    => "メールアドレス",\
    'pass'    => "パスワード",\
    'language'  => "言語",\
    'regist'  => "登録する",\
    'back'    => "変更する",\
    'thanks'  => "ご登録ありがとうございました。",\
    'thanks2' => "して引き続きご利用ください。",
  }

  return l[language]
end

#### HTML top
def html_top_regist( l )
  login_color = "secondary"
  login = "<a href='login.cgi' class=\"text-#{login_color}\">#{l['login']}</a>"

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


#### HTML regist
def html_regist_form( id, mail, pass, msg, aliasu, l )
  option_language = ''
  $LP.each do |e|
    option_language << "<option value='#{e}'>#{e}</option>"
  end
  html = <<-"HTML"
      <div class="container">
        <form action="regist.cgi?mode=confirm" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{l['message']}</p>
          <input type="text" name="id" value="#{id}" maxlength="30" class="form-control login_input" placeholder="#{l['id_rule']}" required autofocus>
          <input type="text" name="pass" value="#{pass}" maxlength="30" class="form-control login_input" placeholder="#{l['pass_rule']}" required>
          <input type="text" name="aliasu" value="#{aliasu}" maxlength="60" class="form-control login_input" placeholder="#{l['a_rule']}">
          <input type="email" name="mail" value="#{mail}" maxlength="60" class="form-control login_input" placeholder="#{l['mail_rule']}">
          <select name="language" class="form-select">
            #{option_language}
          </select>
          <br>
          <input type="submit" value="#{l['submit']}" class="btn btn-success btn-block"></input>
        </form>
      </div>

      <hr>
      <div  class="container" id='rule'></div>
      <script>$( function(){ $( "#rule" ).load( "books/guide/rule.html" );} );</script>
HTML

  puts html
end


#### HTML regist confirm
def html_regist_confirm( id, mail, pass, aliasu, language, l )
    html = <<-"HTML"
      <div class="container">
        <form action="regist.cgi?mode=finish" method="post" class="form-signin login_form">
          <p class="msg_small">#{l['confirm']}</p>
          <table class="table">
              <tr>
                <td>#{l['id']}</td>
                <td>#{id}</td>
              </tr>
              <tr>
                <td>#{l['pass']}</td>
                <td>#{pass}</td>
              </tr>
              <tr>
                <td>#{l['aliase']}</td>
                <td>#{aliasu}</td>
              </tr>
              <tr>
                <td>#{l['mail']}</td>
                <td>#{mail}</td>
              </tr>
              <tr>
                <td>#{l['language']}</td>
                <td>#{language}</td>
              </tr>
          </table>
          <input type="hidden" name="id" value="#{id}">
          <input type="hidden" name="alias" value="#{aliasu}">
          <input type="hidden" name="mail" value="#{mail}">
          <input type="hidden" name="pass" value="#{pass}">
          <input type="hidden" name="language" value="#{language}">
          <input type="submit" value="#{l['regist']}" class="btn btn-warning btn-block"></input>
          <input type="button" value="#{l['back']}" class="btn btn-secondary btn-block" onclick="history.back()"></input>
        </form>
      </div>
HTML

  puts html
end


#### HTML regist finish
def html_regist_finish( l )
    html = <<-"HTML"
      <div class="container">
          <p class="reg_msg">#{l['thanks']}<a href="login.cgi">#{l['login']}<a/>#{l['thanks2']}</p>
      </div>
HTML

  puts html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

l = language_pack( $DEFAULT_LP )
#puts l if @debug


#### Getting GET data
get_data = get_data()

html_head( nil, 0, nil )
html_top_regist( l )

case get_data['mode']
# Confomation of user data
when 'confirm'

  # Checking improper characters
  if /[^0-9a-zA-Z\_]/ =~ @cgi['id']
    msg = "<p class='msg_small_red'>#{l['error1']}</p>"
    html_regist_form( nil, @cgi['mail'], nil, msg, @cgi['aliasu'], l )

  # Checking character limit
  elsif @cgi['id'].size > 30
    msg = "<p class='msg_small_red'>#{l['error2']}</p>"
    html_regist_form( nil, @cgi['mail'], nil, msg, @cgi['aliasu'], l )

  # Checking character limit
  elsif @cgi['id'].size < 4
    msg = "<p class='msg_small_red'>#{l['error3']}</p>"
    html_regist_form( nil, @cgi['mail'], nil, msg, @cgi['aliasu'], l )

  # OK
  else
    # Checking same ID
    r = mdb( "SELECT user FROM #{$MYSQL_TB_USER} WHERE user='#{@cgi['id']}';", false, @debug )
    unless r.first
      html_regist_confirm( @cgi['id'], @cgi['mail'], @cgi['pass'], @cgi['aliasu'], @cgi['language'], l )
    else
      msg = "<p class='msg_small_red'>#{l['error4']}</p>"
      html_regist_form( nil, @cgi['mail'], nil, msg, @cgi['aliasu'], l )
    end
  end


#### Finishing registration of new user
when 'finish'
  # Inserting user information
  aliasu = @cgi['alias']
  aliasu = @cgi['id'] if aliasu == ''
  p @cgi if @debug

  mdb( "INSERT INTO #{$MYSQL_TB_USER} SET user='#{@cgi['id']}', pass='#{@cgi['pass']}', mail='#{@cgi['mail']}',aliasu='#{aliasu}', status=1, language='#{@cgi['language']}', reg_date='#{@datetime}'", false, @debug )

  # Inserting standard palettes
  0.upto( 3 ) do |c|
    mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{@cgi['id']}', name='#{@palette_default_name[c]}', palette='#{@palette_default[c]}';", false, @debug )
  end

  # Inserting new history
  mdb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{@cgi['id']}', his='';", false, @debug )

  # Inserting new SUM
  mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{@cgi['id']}', sum='';", false, @debug )

  # Inserting new meal
  mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{@cgi['id']}', meal='';", false, @debug )

  # Inserting new config
  mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{@cgi['id']}', his_max=200;", false, @debug )

  html_regist_finish( l )

#### Input form
else
  html_regist_form( nil, nil, nil, nil, nil, l )
end

html_foot()
