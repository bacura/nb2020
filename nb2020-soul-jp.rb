#Nutrition browser 2020 soul Japanese pack 0.01b

#==============================================================================
# STATIC
#==============================================================================
@category = ['特殊', '穀類', 'いも・でん粉類', '砂糖・甘味類', '豆類', '種実類', '野菜類', '果実類', 'きのこ類', '藻類', '魚介類', '肉類', '卵類', '乳類', '油脂類', '菓子類', 'し好飲料類', '調味料・香辛料類', '調理・流通食品類', '特殊']

#             0              1                 2                 3                     4                  5                        6                               7               8                                   9                    10                                11                     12              13                                    14                                   15                                     16                     17                   18                    19              20             21              22             23               24                25          26            27            28          29              30            31            32            33               34                 35                  36                  37                           38                         39                            40                41                      42                        43                       44                       45                46                     47                48                49                   50                    51                     52             53                    54                55                56                57                     58
@fct_item = ['FG',          'FN',             'SID',            'Tagnames',           'REFUSE',          'ENERC',                 'ENERC_KCAL',                   'WATER',        'PROTCAA',                          'PROT',              'FATNLEA',                        'CHOLE',               'FAT',         'CHOAVLM',                            'CHOAVL',                            'CHOAVLMF',                            'FIB',                 'POLYL',             'CHOCDF',             'OA',           'ASH',         'NA',            'K',          'CA',            'MG',             'P',         'FE',        'ZN',         'CU',       'MN',           'ID',         'SE',         'CR',         'MO',            'RETOL',            'CARTA',            'CARTB',            'CRYPXB',                   'CARTBEQ',                 'VITA_RAE',                   'VITD',           'TOCPHA',                'TOCPHB',                'TOCPHG',                'TOCPHD',                'VITK',           'THIAHCL',            'RIBF',            'NIA',            'NE',                 'VITB6A',            'VITB12',              'FOL',         'PANTAC',             'BIOT',           'VITC',           'ALC',            'NACL_EQ',             'Notice']
@fct_name = {'FG'=>'食品群', 'FN'=>'食品番号', 'SID'=>'索引番号', 'Tagnames'=>'食品名', 'REFUSE'=>'廃棄率', 'ENERC'=>'エネルギー(kJ)',  'ENERC_KCAL'=>'エネルギー(kcal)',  'WATER'=>'水分', 'PROTCAA'=>'アミノ酸組成によるたんぱく質', 'PROT'=>'たんぱく質',  'FATNLEA'=>'トリアシルグリセロール当量', 'CHOLE'=>'コレステロール',  'FAT'=>'脂質', 'CHOAVLM'=>'利用可能炭水化物(単糖当量)', 'CHOAVL'=>'利用可能炭水化物(質量計)', 'CHOAVLMF'=>'利用可能炭水化物(差引き法)', 'FIB'=>'食物繊維総量',  'POLYL'=>'糖アルコール', 'CHOCDF'=>'炭水化物', 'OA'=>'有機酸',  'ASH'=>'灰分', 'NA'=>'ナトリウム', 'K'=>'カリウム', 'CA'=>'カルシウム', 'MG'=>'マグネシウム', 'P'=>'リン',  'FE'=>'鉄',  'ZN'=>'亜鉛', 'CU'=>'銅',  'MN'=>'マンガン', 'ID'=>'ヨウ素', 'SE'=>'セレン', 'CR'=>'クロム', 'MO'=>'モリブデン', 'RETOL'=>'レチノール', 'CARTA'=>'α-カロテン', 'CARTB'=>'β-カロテン', 'CRYPXB'=>'β-クリプトキサンチン', 'CARTBEQ'=>'β-カロテン当量', 'VITA_RAE'=>'レチノール活性当量', 'VITD'=>'ビタミンD', 'TOCPHA'=>'α-トコフェロール', 'TOCPHB'=>'β-トコフェロール',  'TOCPHG'=>'γ-トコフェロール', 'TOCPHD'=>'δ-トコフェロール', 'VITK'=>'ビタミンK', 'THIAHCL'=>'ビタミンB1', 'RIBF'=>'ビタミンB2', 'NIA'=>'ナイアシン', 'NE'=>'ナイアシン当量',   'VITB6A'=>'ビタミンB6', 'VITB12'=>'ビタミンB12', 'FOL'=>'葉酸', 'PANTAC'=>'パントテン酸', 'BIOT'=>'ビオチン', 'VITC'=>'ビタミンC', 'ALC'=>'アルコール', 'NACL_EQ'=>'食塩相当量', 'Notice'=>'備考'}
@fct_unit = {'FG'=>nil,     'FN'=>nil,        'SID'=>nil,       'Tagnames'=>nil,      'REFUSE'=>'%',     'ENERC'=>'kJ',           'ENERC_KCAL'=>'kcal',           'WATER'=>'g',   'PROTCAA'=>'g',                     'PROT'=>'g',         'FATNLEA'=>'g',                   'CHOLE'=>'mg',         'FAT'=>'g',    'CHOAVLM'=>'g',                       'CHOAVL'=>'g',                       'CHOAVLMF'=>'g',                       'FIB'=>'g',            'POLYL'=>'g',        'CHOCDF'=>'g',        'OA'=>'g',      'ASH'=>'g',    'NA'=>'mg',      'K'=>'mg',    'CA'=>'mg',      'MG'=>'mg',       'P'=>'mg',   'FE'=>'mg',  'ZN'=>'mg',   'CU'=>'mg', 'MN'=>'mg',     'ID'=>'μg',   'SE'=>'μg',   'CR'=>'μg',   'MO'=>'μg',      'RETOL'=>'μg',      'CARTA'=>'μg',      'CARTB'=>'μg',       'CRYPXB'=>'μg',             'CARTBEQ'=>'μg',          'VITA_RAE'=>'μg',             'VITD'=>'μg',     'TOCPHA'=>'mg',          'TOCPHB'=>'mg',          'TOCPHG'=>'mg',          'TOCPHD'=>'mg',          'VITK'=>'μg',     'THIAHCL'=>'mg',      'RIBF'=>'mg',      'NIA'=>'mg',      'NE'=>'mg',          'VITB6A'=>'mg',      'VITB12'=>'μg',        'FOL'=>'μg',   'PANTAC'=>'mg',       'BIOT'=>'μg',     'VITC'=>'mg',     'ALC'=>'g',      'NACL_EQ'=>'g',          'Notice'=>nil}
@fct_frct = {'FG'=>nil,     'FN'=>nil,        'SID'=>nil,       'Tagnames'=>nil,      'REFUSE'=>nil,     'ENERC'=>0,              'ENERC_KCAL'=>0,                'WATER'=>1,     'PROTCAA'=>1,                       'PROT'=>1,           'FATNLEA'=>1,                     'CHOLE'=>0,            'FAT'=>1,      'CHOAVLM'=>1,                         'CHOAVL'=>1,                         'CHOAVLMF'=>1,                         'FIB'=>1,              'POLYL'=>1,          'CHOCDF'=>1,          'OA'=>1,        'ASH'=>1,      'NA'=>0,         'K'=>0,       'CA'=>0,         'MG'=>0,          'P'=>0,      'FE'=>1,     'ZN'=>1,      'CU'=>2,    'MN'=>2,        'ID'=>0,      'SE'=>0,      'CR'=>0,      'MO'=>0,         'RETOL'=>0,         'CARTA'=>0,         'CARTB'=>0,          'CRYPXB'=>0,                'CARTBEQ'=>0,             'VITA_RAE'=>0,                'VITD'=>1,        'TOCPHA'=>1,             'TOCPHB'=>1,             'TOCPHG'=>1,             'TOCPHD'=>1,             'VITK'=>0,        'THIAHCL'=>2,         'RIBF'=>2,         'NIA'=>1,         'NE'=>1,             'VITB6A'=>2,         'VITB12'=>1,           'FOL'=>0,      'PANTAC'=>2,          'BIOT'=>1,        'VITC'=>0,        'ALC'=>1,        'NACL_EQ'=>1,            'Notice'=>nil}
@fct_default5 = [6, 9, 12, 18, 57]
@fct_start = 5
$FCT_START = { 'jp' => @fct_start }
@fct_end = 57
$FCT_END = { 'jp' => @fct_end }


@recipe_type = ['未設定','和食','洋食','中華','イタリアン','フレンチ','エスニック']
@recipe_role = ['未設定','主食','主菜','副菜','汁物','デザート・おやつ','飲み物','調味料']
@recipe_tech = ['未設定','茹でる・煮る・炊く','直火・炙る','炒める・ソテー','蒸す','揚げる','和える','生・非加熱','冷蔵・冷凍','オーブン・グリル','電子レンジ']
@recipe_time = ['未設定','～5','～10','～15','～20','～30','～45','～60','～120','121～']
@recipe_cost = ['未設定','50円未満','100円未満','150円未満','200円未満','300円未満','400円未満','500円未満','600円未満','800円未満','1000円未満', '1000円以上']

#         0     1    2    3       4       5     6     7       8     9       10    11    12    13    14     15       16    17
@unit = ['g','kcal','ml','小さじ','大さじ','カップ','合','切身S','切身M','切身L','個S','個M','個L','SV', '単位', '廃棄前', 'cm', '標準']

#              0    1           2         3     4       5
@sub_group = ['','緑黄色野菜','普通牛乳','味噌','醤油','食塩']

#           0    1   2       3     4     5    6    7       8        9     10    11      12          13           14     15    16    17    18   19      20    21     22     23       24    25      26      27     28
@allergy = ['','えび','かに','小麦','そば','卵','乳','落花生','あわび','いか','いくら','オレンジ','カシューナッツ','キウイフルーツ','牛肉','くるみ','ごま','さけ','さば','大豆','鶏肉','バナナ','豚肉','まつたけ','もも','やまいも','りんご','ゼラチン','アーモンド']

#          0        1     2      3      4    5    6    7    8    9   10   11
@color = ['未指定','赤','ピンク','オレンジ','黄','緑','青','紫','茶','白','黒','透明']

#           0      1      2       3        4           5         6      7   8       9
@account = ['退会','一般','ギルメン','guest', 'ギルメン・萌','ギルメン・旬','娘','-','サブマス','ギルマス']

#           0           1       2       3       4     5         6       7         8              9      10
@kex_item = ['未設定', '独自→', '身長', '体重', 'BMI', '体脂肪率', '腹囲', '首回り', '骨盤上部周囲', '便通', 'METs']
@kex_unit = ['',       ''    , 'cm'  ,  'kg',    '',        '%',  'cm',    'cm',          'cm',   'BS',     '']

@something = {'?--'=>'何か食べた（微盛）', '?-'=>'何か食べた（小盛）', '?='=>'何か食べた（並盛）', '?+'=>'何か食べた（大盛）', '?++'=>'何か食べた（特盛）', '?0'=>'何も食べない'}


#==============================================================================
# HTML header
#==============================================================================
def html_head( interrupt, status, sub_title )
  refresh = ''
  refresh = '<meta http-equiv="refresh" content="0; url=index.cgi">' if interrupt == 'refresh'

  js_guild = ''
  js_guild = "<script type='text/javascript' src='#{$JS_PATH}/guild.js'></script>" if status >= 3

  js_shun = ''
  js_shun = "<script type='text/javascript' src='#{$JS_PATH}/shun.js'></script>" if status >= 5

  js_master = ''
  js_master = "<script type='text/javascript' src='#{$JS_PATH}/master.js'></script>" if status >= 8

  html = <<-"HTML"
<!DOCTYPE html>
<head>
  #{refresh}
  <title>栄養ブラウザ #{sub_title}</title>
  <meta charset="UTF-8">
  <meta name="keywords" content="栄養,個人,栄養士,無料,フリー,Web,サービス,nutrition, Nutritionist, food,検索,計算,解析,評価,栄養計算">
  <meta name="description" content="食品成分表の検索,栄養計算,栄養評価, analysis, calculation,無料のwebサイト">
  <meta name="robots" content="index,follow">
  <meta name="author" content="Shinji Yoshiyama@ばきゅら京都Lab">
  <!-- bootstrap -->
  <link rel="stylesheet" href="bootstrap-dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="#{$CSS_PATH}/core.css">

<!-- Jquery -->
  <script type="text/javascript" src="./jquery-3.6.0.min.js"></script>
<!-- bootstrap -->
  <script type="text/javascript" src="bootstrap-dist/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="#{$JS_PATH}/core.js"></script>
  <script type='text/javascript' src='#{$JS_PATH}/recipe.js'></script>
  #{js_guild}
  #{js_shun}
  #{js_master}

  <!--#{tracking()}-->

</head>

<body class="body">
  <span class="world_frame" id="world_frame">
HTML

  puts html
end

#==============================================================================
# HTML footer
#==============================================================================
def html_foot()
    html = <<-"HTML"
    <br>
      <footer class="footer">
        <div align="center">
          <a href="https://neg.bacura.jp">日本えいようギルド</a>
          <a href="https://bacura.jp"><img src="https://bacura.jp/img/BKL_banner_h125.png" alt="ばきゅら京都Lab"></a>
        </div>
      </footer>
    </span>
  </body>
</html>
HTML

  puts html
end

#==============================================================================
# DATE & TIME
#==============================================================================
@time_now = Time.now
@datetime = @time_now.strftime("%Y-%m-%d %H:%M:%S")

#==============================================================================
# MEDIA
#==============================================================================
$WM_FONT = 'さざなみゴシック'