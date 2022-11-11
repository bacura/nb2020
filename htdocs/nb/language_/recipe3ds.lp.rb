# Language pack for recipe 3D plotter 0.00b (2022/11/05)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'plot_size' => "プロットサイズ",\
		'y_log' 	=> "Y軸Log",\
		'dsp_label'	=> "ラベル表示",\
		'plot'		=> "プロット",\
		'more'		=> "以上",\
		'less'		=> "以下",\
		'xcomp'		=> "X軸成分",\
		'ycomp'		=> "y軸成分",\
		'zcomp'		=> "z軸成分",\
		'range'		=> "表示範囲",\
		'style'		=> "料理スタイル",\
		'role'		=> "献立区分",\
		'tech'		=> "調理区分",\
		'time'		=> "表目安時間(分)",\
		'cost'		=> "目安費用(円)",\
		'all'		=> "全て",\
		'draft'		=> "下書き",\
		'protect'	=> "保護",\
		'public'	=> "公開",\
		'no_mark'	=> "無印",\
		'public_'	=> "公開(他ユーザー)",\
		'no_def'	=> "未設定",\
		'all_ns'	=> "全て（調味系除く）",\
		'chomi'		=> "[ 調味％ ]",\
		'reset'		=> "リセット"
	}

	return l[language]
end
