// Recipe java script for nb2020 0.03b
////////////////////////////////////////////////////////////////////////////////////////
// Chopping boad interface////////////////////////////////////////////////////////////////////////

// Add food into sum, and reload CB counter
var addingCB = function( fn, weight_id, food_name ){
	if( weight_id != '' ){
		var weight = document.getElementById( weight_id ).value;
	}
	$.post( "cboardm.cgi", { food_no:fn, food_weight:weight, mode:'add' }, function( data ){
		$( "#CBN" ).html( data );
		refreshCBN();
		if( fn != '' ){ displayVIDEO( '+' + food_name ); }
	});
};


// Only reload CB number
var refreshCBN = function(){
	$.post( "cboardm.cgi", { mode:'refresh' }, function( data ){ $( "#CBN" ).html( data );});
};


////////////////////////////////////////////////////////////////////////////////////////
// Chopping boad ////////////////////////////////////////////////////////////////////////

// 変更ボタンを押してsumの食品を変更する
var changingCB = function( fn, base_fn ){
	if( fn !='' ){
		var weight = document.getElementById( "weight" ).value;
		$.post( "cboardm.cgi", { food_no:fn, food_weight:weight, base_fn:base_fn, mode:'change' }, function( data ){
			$( "#CBN" ).html( data );
			displayVIDEO( fn + 'has modified' );

			$.post( "cboard.cgi", { command:'refresh', code:'' }, function( data ){
				$( "#L1" ).html( data );

				flashBW();
				dl1 = true;
				displayBW();
			});
		});
	}
};


// Display CB sum in L1
var initCB = function( com, code, recipe_user ){
	$.post( "cboard.cgi", { command:com, code:code, recipe_user:recipe_user }, function( data ){
		$( "#L1" ).html( data );
		refreshCBN();

		flashBW();
		dl1 = true;
		displayBW();
	});
};


// Clear foods, and reload CB counter
var clearCB = function( order, code ){
	if( order == 'all'){
		if( document.getElementById( 'all_check' ).checked ){
			$.post( "cboard.cgi", { command:'clear', food_check:'all', code:code }, function( data ){
				$( "#L1" ).html( data );
				refreshCBN();
			});
			flashBW();
			dl1 = true;
			displayBW();
		} else{
			displayVIDEO( '(>_<)cheack!' );
		}
	} else{
		$.post( "cboard.cgi", { command:'clear', order:order, code:code }, function( data ){
			$( "#L1" ).html( data );
			refreshCBN();
		});
	}
};


// 食品上ボタンを押してなま板リストを更新してL1に表示
var upperCB = function( order, code ){
	$.post( "cboard.cgi", { command:'upper', order:order, code:code }, function( data ){ $( "#L1" ).html( data );});
};


// まな板の食品下ボタンを押してL1にリストを更新
var lowerCB = function( order, code ){
	$.post( "cboard.cgi", { command:'lower', order:order, code:code }, function( data ){ $( "#L1" ).html( data );});
};


// Changing dish number
var dishCB = function( code ){
	var dish_num = document.getElementById( "dish_num" ).value;
	$.post( "cboard.cgi", { command:'dish', code:code, dish_num:dish_num }, function( data ){ $( "#L1" ).html( data );});
};


// Adjusting total food weight
var weightAdj = function( code ){
	var weight_adj = document.getElementById( "weight_adj" ).value;
	$.post( "cboard.cgi", { command:'wadj', code:code, weight_adj:weight_adj }, function( data ){ $( "#L1" ).html( data );});
	displayVIDEO( 'Adjusted' );
};


// Adjusting total food energy
var energyAdj = function( code ){
	var energy_adj = document.getElementById( "energy_adj" ).value;
	$.post( "cboard.cgi", { command:'eadj', code:code, energy_adj:energy_adj }, function( data ){ $( "#L1" ).html( data );});
		displayVIDEO( 'Adjusted' );
};


// Adjusting total food salt
var saltAdj = function( code ){
	var salt_adj = document.getElementById( "salt_adj" ).value;
	$.post( "cboard.cgi", { command:'sadj', code:code, salt_adj:salt_adj }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( 'Adjusted' );
	});
};


// Adjusting feeding rate by food loss
var lossAdj = function( code ){
	var loss_adj = document.getElementById( "loss_adj" ).value;
	$.post( "cboard.cgi", { command:'ladj', code:code, loss_adj:loss_adj }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( 'Adjusted' );
	});
};


// Sorting sum list by food weight
var sortCB = function( code ){
	$.post( "cboard.cgi", { command:'sort', code:code }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( 'Sorted' );
	});
};


// まな板の食品番号追加ボタンを押して食品を追加してL1にリストを表示。そしてカウンターも更新
var recipeAdd = function( code ){
	var fn = document.getElementById( "food_add" ).value;
	$.post( "cboard.cgi", { command:'add', fn:fn, code:code }, function( data ){
		$( "#L1" ).html( data );
		refreshCBN();
	});
};


// まな板の調味％ボタンを押してプリセット食品を追加してL1にリストを表示。そしてカウンターも更新
var seasoningAdd = function( code ){
	var seasoning = document.getElementById( "seasoning" ).value;
	$.post( "cboard.cgi", { command:'seasoning', seasoning:seasoning, code:code }, function( data ){
		$( "#L1" ).html( data );
		refreshCBN();
	});
};


// まな板の重量情報更新でL1にリストを更新
var weightCB = function( order, unitv_id, unit_id, food_init_id, food_rr_id, code ){
	var unitv = document.getElementById( unitv_id ).value;
	var unit = document.getElementById( unit_id ).value;
	var food_init = document.getElementById( food_init_id ).value;
	var food_rr = document.getElementById( food_rr_id ).value;

	$.post( "cboard.cgi", { command:'weight', order:order, unitv:unitv, unit:unit, code:code, food_init:food_init, food_rr:food_rr }, function( data ){ $( "#L1" ).html( data );});
};


// まな板の初期状態更新で裏で更新
var initCB_SS = function( order, unitv_id, unit_id, food_init_id, food_rr_id, code ){
	var unitv = document.getElementById( unitv_id ).value;
	var unit = document.getElementById( unit_id ).value;
	var food_init = document.getElementById( food_init_id ).value;
	var food_rr = document.getElementById( food_rr_id ).value;

	$.post( "cboard.cgi", { command:'weight', order:order, unitv:unitv, unit:unit, code:code, food_init:food_init, food_rr:food_rr }, function( data ){});
};


// まな板の食品チェックボックスを押してL1にリストを更新
var checkCB = function( order, code, check_id ){
	var checked = 0;
	if( document.getElementById( check_id ).checked ){ checked = 1; }
	$.post( "cboard.cgi", { command:'check_box', order:order, food_check:checked, code:code }, function( data ){});
};


// Switching all check box
var allSwitch = function( code ){
	var allSwitch = 0;
	if( document.getElementById( 'switch_all' ).checked ){ allSwitch = 1; }
	$.post( "cboard.cgi", { command:'allSwitch', code:code, allSwitch:allSwitch }, function( data ){ $( "#L1" ).html( data );});
};


// Quick Save
var quickSave = function( code ){
	$.post( "cboard.cgi", { command:'quick_save', code:code }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( 'Saved' );
	});
};


// GN Exchange
var gnExchange = function( code ){
	if( document.getElementById( 'gn_check' ).checked ){
		$.post( "cboard.cgi", { command:'gn_exchange', code:code }, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( 'Adjusted' );
		});
	} else{
		displayVIDEO( 'Check!!(>_<)' );
	}
};


// まな板からでL5閲覧ウインドウを表示する。
var cb_summon = function( key, weight, base_fn ){
	$.get( "square.cgi", { channel:"fctb_l5", food_key:key, frct_mode:0, food_weight:weight, base:'cb', base_fn:base_fn }, function( data ){
		$( "#L5" ).html( data );

		flashBW();
		dl5 = true;
		displayBW();
	});
};

// Chomi% category
var chomiSelect =  function(){
	var code = document.getElementById( "recipe_code" ).value;
	var chomi_selected = document.getElementById( "chomi_selected" ).value;
	$.post( "cboard.cgi", { command:'chomi', code:code, chomi_selected:chomi_selected }, function( data ){ $( "#chomi_cell" ).html( data );});
};

// Chomi% add
var chomiAdd =  function(){
	var code = document.getElementById( "recipe_code" ).value;
	var chomi_selected = document.getElementById( "chomi_selected" ).value;
	var chomi_code = document.getElementById( "chomi_code" ).value;
	$.post( "cboard.cgi", { command:'chomis', code:code, chomi_selected:chomi_selected, chomi_code:chomi_code }, function( data ){ $( "#L1" ).html( data );});
};


////////////////////////////////////////////////////////////////////////////////
// Recipe ////////////////////////////////////////////////////////////////////////

// レシピ編集のレシピボタンを押してL2にレシピを表示
var recipeEdit = function( com, code ){
	$.post( "recipe.cgi", { command:com, code:code }, function( data ){
		$( "#L2" ).html( data );
		dl2 = true;
		displayBW();
	});
	$.post( "photo.cgi", { command:'view_series', code:code, base:'recipe' }, function( data ){
		$( "#L3" ).html( data );
		dl3 = true;
		displayBW();
	});
};


// レシピ編集の公開ボタンを押して
var recipeBit_public = function(){
	if( document.getElementById( "public" ).checked ){
		document.getElementById( "protect" ).checked = true;
		document.getElementById( "draft" ).checked = false;
	}
};

// レシピ編集の保護ボタンを押して
var recipeBit_protect = function(){
	if( document.getElementById( "protect" ).checked ){
		document.getElementById( "draft" ).checked = false;
	}
};

// レシピ編集の仮組ボタンを押して
var recipeBit_draft = function(){
	if( document.getElementById( "draft" ).checked ){
		document.getElementById( "protect" ).checked = false;
		document.getElementById( "public" ).checked = false;
	}
};


// レシピ編集の保存ボタンを押してレシピを保存、そしてL2にリストを再表示
var recipeSave = function( code ){
	var recipe_name = document.getElementById( "recipe_name" ).value;
	if( recipe_name == '' ){
		displayVIDEO( 'Recipe name! (>_<)');
	}
	else{
		var type = document.getElementById( "type" ).value;
		var role = document.getElementById( "role" ).value;
		var tech = document.getElementById( "tech" ).value;
		var time = document.getElementById( "time" ).value;
		var cost = document.getElementById( "cost" ).value;
		var protocol = document.getElementById( "protocol" ).value;

		if( document.getElementById( "public" ).checked ){ var public = 1 }
		if( document.getElementById( "protect" ).checked ){ var protect = 1 }
		if( document.getElementById( "draft" ).checked ){ var draft = 1 }

		$.post( "recipe.cgi", { command:'save', code:code, recipe_name:recipe_name, type:type, role:role, tech:tech, time:time, cost:cost, protocol:protocol, public:public, protect:protect, draft:draft }, function( data ){
			$( "#L2" ).html( data );
			$.post( "cboard.cgi", { command:'init', code:'' }, function( data ){ $( '#L1' ).html( data );});
			$.post( "photo.cgi", { command:'view_series', code:'', base:'recipe' }, function( data ){ $( "#L3" ).html( data );});
			displayVIDEO( recipe_name );
		});
	}
};


// レシピ編集の保存ボタンを押してレシピを保存、そしてL2にリストを再表示
var recipeProtocol = function( code ){
	if( document.getElementById( "protect" ).checked ){ var protect = 1; }
	if( code != '' && protect != 1 ){
		var protocol = document.getElementById( "protocol" ).value;
		$.post( "recipe.cgi", { command:'protocol', code:code, protocol:protocol }, function( data ){
			$( '#L2' ).html( data );
			displayVIDEO( '●' );
		});
	}
};

////////////////////////////////////////////////////////////////////////////////////
// Recipe list ////////////////////////////////////////////////////////////////////////

// Dosplaying recipe list with reset
var recipeList = function( com ){
	$.post( "recipel.cgi", { command:com }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};


// Refreshing list
var fxRLR = function( command, range, type, role, tech, time, cost, page ){
	$.post( "recipel.cgi", { command:command, range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page }, function( data ){ $( "#L1" ).html( data );});
};


// Dosplaying recipe list with narrow down
var recipeListP = function( page ){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;
	fxRLR( 'limit', range, type, role, tech, time, cost, page );
};


// Displaying recipe list after delete
var recipeDelete = function( code, page ){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;

	if( document.getElementById( code ).checked ){
		$.post( "recipel.cgi", { command:'delete', code:code, range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page }, function( data ){
			fxRLR( 'limit', range, type, role, tech, time, cost, page );
			displayVIDEO( 'Removed' );
		});
	} else{
		displayVIDEO( 'Check! (>_<)' );
	}
};


// Generationg subSpecies
var recipeImport = function( com, code, page ){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;

	$.post( "recipel.cgi", { command:com, code:code, range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( '+recipe' );
	});
};


///////////////////////////////////////////////////////////////////////////////////
// 成分計算 ////////////////////////////////////////////////////////////////////////

// まな板の成分計算表ボタンを押してL2にリストを表示
var calcView = function( code ){
	$.post( "calc.cgi", { command:'view', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 成分計算表の再計算ボタンを押してL2にリストを表示
var recalcView = function( code ){
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "calc.cgi", { command:'view', code:code, palette:palette, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Recalc' );
	});
};


///////////////////////////////////////////////////////////////////////////////////
// 原価計算 ////////////////////////////////////////////////////////////////////////

// まな板の原価計算表ボタンを押してL2にリストを表示
var priceView = function( code ){
	$.post( "price.cgi", { command:'view', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 原価計算表の購入量変更でL2に原価表を更新
var changeFV = function( code, fvid, food_no ){
	var food_volume = document.getElementById( fvid ).value;
	$.post( "price.cgi", { command:'changeFV', code:code, food_volume:food_volume, food_no:food_no }, function( data ){ $( "#L2" ).html( data );});
};

// 原価計算表の支払金額変更でL2に原価表を更新
var changeFP = function( code, fpid, food_no ){
	var food_price = document.getElementById( fpid ).value;
	$.post( "price.cgi", { command:'changeFP', code:code, food_price:food_price, food_no:food_no }, function( data ){ $( "#L2" ).html( data );});
};

// 原価計算表のマスター価格を適用してL2に原価表を更新
var pricemAdpt = function( code ){
	$.post( "price.cgi", { command:'adpt_master', code:code }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'マスター価格を適用' );
	});
};

// 原価計算表のマスター価格登録（でL2に原価表を更新）
var pricemReg = function( code ){
	$.post( "price.cgi", { command:'reg_master', code:code }, function( data ){
//		$( "#L2" ).html( data );
		displayVIDEO( 'マスター価格に登録' );
	});
};

// 原価計算表の価格を元にレシピの価格区分を変更
var recipeRef = function( code ){
	$.post( "price.cgi", { command:'ref_recipe', code:code }, function( data ){
//		$( "#L2" ).html( data );
		displayVIDEO( '価格区分へ反映' );
	});
};

// 原価計算表の初期化ボタンでL2に原価表を更新
var clearCT = function( code ){
	if( document.getElementById( "clearCT_check" ).checked ){
		$.post( "price.cgi", { command:'clearCT', code:code }, function( data ){ $( "#L2" ).html( data );});
	}else{
		displayVIDEO( '(>_<) check!' );
	}
};

///////////////////////////////////////////////////////////////////////////////////
// Lucky star input ////////////////////////////////////////////////////////////////////////

// Lucky☆入力ボタンを押してL2に入力画面を表示、そしてL1を非表示にする
var luckyInput = function(){
	$.post( "lucky.cgi", { command:'form' }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// Lucky☆転送ボタンを押してL2に確認画面を表示
var luckyAnalyze = function(){
	var lucky_data = document.getElementById( 'lucky_data' ).value;
	$.post( "lucky.cgi", { command:'analyze', lucky_data:lucky_data }, function( data ){
		$( "#L2" ).html( data );
		$.post( "cboard.cgi", { command:'init', code:'' }, function( data ){ $( '#L1' ).html( data );});
		refreshCBN();
		displayVIDEO( 'Lucky?' );
	});
};

///////////////////////////////////////////////////////////////////////////////////
// Foodize ////////////////////////////////////////////////////////////////////////

// 成分計算表の食品化ボタンを押してL3に擬似食品フォームを表示
var Pseudo_R2F = function( code ){
	$.post( "pseudo_r2f.cgi", { command:'form', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 食品化フォームの保存ボタンを押して保存してL3を消す。
var savePseudo_R2F = function( code ){
	var food_name = document.getElementById( "r2ffood_name" ).value;
	if( food_name != '' ){

		var food_group = document.getElementById( "r2ffood_group" ).value;
		var class1 = document.getElementById( "r2fclass1" ).value;
		var class2 = document.getElementById( "r2fclass2" ).value;
		var class3 = document.getElementById( "r2fclass3" ).value;
		var tag1 = document.getElementById( "r2ftag1" ).value;
		var tag2 = document.getElementById( "r2ftag2" ).value;
		var tag3 = document.getElementById( "r2ftag3" ).value;
		var tag4 = document.getElementById( "r2ftag4" ).value;
		var tag5 = document.getElementById( "r2ftag5" ).value;

		$.post( "pseudo_r2f.cgi", {
			command:'save', code:code,
			food_name:food_name, food_group:food_group, class1:class1, class2:class2, class3:class3, tag1:tag1,
			tag2:tag2, tag3:tag3, tag4:tag4, tag5:tag5
		}, function( data ){
			$( "#L2" ).html( data );
			displayVIDEO( 'Foodized' );
		});
	}else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};

///////////////////////////////////////////////////////////////////////////////////
// 印刷用清書レシピ /////////////////////////////////////////////////////////////////

// レシピ帳の印刷ボタンを押してL2に印刷画面テンプレートを表示
var print_templateSelect = function( code ){
	$.post( "print.cgi", { command:'select', code:code }, function( data ){ $( "#L2" ).html( data );});
	document.getElementById( "L1" ).style.display = 'none';
	document.getElementById( "L2" ).style.display = 'block';
};

// 印刷テンプレート画面の戻るボタンを押してレシピ帳に復帰
var print_templateReturen = function(){
	document.getElementById( "L1" ).style.display = 'block';
	document.getElementById( "L2" ).style.display = 'none';
};

// 印刷テンプレート画面の印刷表示ボタンを押して新規タブに印刷画面を表示する。
var openPrint = function( uname, code, template, dish ){
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }

	if( document.getElementById( "csc" ).checked ){
		var csc = document.getElementById( "csc" ).value;
		var url = 'printv.cgi?&c=' + code + '&t=' + template + '&d=' + dish + '&p=' + palette + '&fa=' + frct_accu + '&ew=' + ew_mode + '&fm=' + frct_mode + '&cs=' + csc;
	}else{
		var url = 'printv.cgi?&c=' + code + '&t=' + template + '&d=' + dish + '&p=' + palette + '&fa=' + frct_accu + '&ew=' + ew_mode + '&fm=' + frct_mode;
	}
	window.open( url, 'print' );
	displayVIDEO( 'Printing page was opend on the another tab' );
};


/////////////////////////////////////////////////////////////////////////////////
// Set menu ////////////////////////////////////////////////////////////////////////

// 献立追加ボタンを押してmealにレシピを追加して、まな献立カウンタを増やす
var addingMeal = function( recipe_code, recipe_name ){
	$.post( "mealm.cgi", { recipe_code:recipe_code }, function( data ){
		$( "#MBN" ).html( data );
		if( recipe_code != '' ){ displayVIDEO( '+' + recipe_name); }
	});
};


// 献立ボタンを押してL1にリストを表示
var initMeal = function( com, code ){
	$.post( "meal.cgi", { command:com, code:code }, function( data ){
		$( "#L1" ).html( data );
		flashBW();
		dl1 = true;
		displayBW();
	});
};

// 献立クリアボタンを押してL1にリストを更新、そしてまな献立カウンターの更新
var clear_meal = function( order, code ){
	if( order == 'all'){
		if( document.getElementById( 'meal_all_check' ).checked ){
			$.post( "meal.cgi", { command:'clear', order:'all', code:code }, function( data ){
				$( "#L1" ).html( data );
				addingMeal( '' );

				displayVIDEO( 'Menu cleared' );
				flashBW();
				dl1 = true;
				displayBW();
			});
		} else{
			displayVIDEO( 'Check! (>_<)' );
		}
	} else{
		$.post( "meal.cgi", { command:'clear', order:order, code:code }, function( data ){
			$( "#L1" ).html( data );
			addingMeal( '' );
		});
	}
};


// 献立上ボタンを押してL1に献立リストを更新
var upper_meal = function( order, code ){
	$.post( "meal.cgi", { command:'upper', order:order, code:code }, function( data ){ $( "#L1" ).html( data );});
};


// 献立下ボタンを押してL1に献立リストを更新
var lower_meal = function( order, code ){
	$.post( "meal.cgi", { command:'lower', order:order, code:code }, function( data ){ $( "#L1" ).html( data );});
};

////////////////////////////////////////////////////////////////////////////////
// セットメニュー ////////////////////////////////////////////////////////////////////////

// 献立編集のレシピボタンを押してL2にレシピを表示
var menuEdit = function( com, code ){
	$.post( "menu.cgi", { command:com, code:code }, function( data ){
		$( "#L2" ).html( data );
		dl2 = true;
		displayBW();
	});
	$.post( "photo.cgi", { command:'view_series', code:code, base:'menu' }, function( data ){
		$( "#L3" ).html( data )
		dl3 = true;
		displayBW();
	});
};


// メニュー編集の保存ボタンを押してレシピを保存、そしてL2にリストを再表示
var menuSave = function( code ){
	var menu_name = document.getElementById( "menu_name" ).value;
	if( menu_name == '' ){
		displayVIDEO( 'Menu name! (>_<)' );
	}
	else{
		if( document.getElementById( "public" ).checked ){ var public = 1 }
		if( document.getElementById( "protect" ).checked ){ var protect = 1 }
		var label = document.getElementById( "label" ).value;
		var new_label = document.getElementById( "new_label" ).value;
		var memo = document.getElementById( "memo" ).value;

		$.post( "menu.cgi", { command:'save', code:code, menu_name:menu_name, public:public, protect:protect, label:label, new_label:new_label, memo:memo }, function( data ){
			$( "#L2" ).html( data );
			$.post( "meal.cgi", { command:'init', code:code }, function( data ){$( '#L1' ).html( data );});
			displayVIDEO( menu_name );
		});
	}
};


// Copying lebel to new label
var copyLabel = function(){
	document.getElementById( "new_label" ).value = document.getElementById( "label" ).value;
};


// Changing label set
var switchLabelset = function( normal_label_c, school_label_c ){
	var label_status = document.getElementById( 'normal_label0' ).style.display;
	if( school_label_c > 0){
		if( label_status == 'inline' ){
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label' + i ).style.display = 'none';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label' + i ).style.display = 'inline';
			}
			document.getElementById( 'label' ).selectedIndex = normal_label_c + 1;
		}else{
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label' + i ).style.display = 'inline';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label' + i ).style.display = 'none';
			}
			document.getElementById( 'label' ).selectedIndex = 0;
		}
	}
}

////////////////////////////////////////////////////////////////////////////////////
// Set menu list ////////////////////////////////////////////////////////////////////////

// まな板のレシピ読み込みボタンを押してL1に献立リストを表示
var menuList = function( page ){
	$.post( "menul.cgi", { command:'view', page:page }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};


// まな板のレシピ読み込みボタンを押してL1に献立リストを表示
var menuList2 = function( page ){
	var range = document.getElementById( "range" ).value;
	var label = document.getElementById( "label_list" ).value;
	$.post( "menul.cgi", { command:'view2', page:page, range:range, label:label }, function( data ){ $( "#L1" ).html( data );});
};


// まな板の削除ボタンを押してレシピを削除し、L1にリストを再表示
var menuDelete = function( code, menu_name ){
	if( document.getElementById( code ).checked ){
		$.post( "menul.cgi", { command:'delete', code:code }, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( menu_name );
		});
	} else{
		displayVIDEO( 'Check! (>_<)' );
	}
};


// まな板のインポートボタンを押してレシピをインポートし、L1にリストを再表示
var menuImport = function( code ){
	$.post( "menul.cgi", { command:'import', code:code }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( code );
	});
};


// Changing label set
var switchLabelsetl = function( normal_label_c, school_label_c ){
	var label_status = document.getElementById( 'normal_label_list0' ).style.display;
	if( school_label_c > 0){
		if( label_status == 'inline' ){
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label_list' + i ).style.display = 'none';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label_list' + i ).style.display = 'inline';
			}
			document.getElementById( 'label_list' ).selectedIndex = normal_label_c + 1;
		}else{
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label_list' + i ).style.display = 'inline';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label_list' + i ).style.display = 'none';
			}
			document.getElementById( 'label_list' ).selectedIndex = 0;
		}
	}
}

///////////////////////////////////////////////////////////////////////////////////
// 献立の成分計算 ////////////////////////////////////////////////////////////////////////

// 献立の成分計算表ボタンを押してL2にリストを表示
var menuCalcView = function( code ){
	$.post( "menu-calc.cgi", { command:'view', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 献立の成分計算表の再計算ボタンを押してL2にリストを表示
var menuRecalcView = function( code ){
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "menu-calc.cgi", { command:'view', code:code, palette:palette, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Recalc' );
	});
};


///////////////////////////////////////////////////////////////////////////////////
// Analysis of menu ////////////////////////////////////////////////////////////////////////

// Analysis of menu
var menuAnalysis = function( code ){
	$.post( "menu-analysis.cgi", { command:'', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// Reanalysis of menu
var menuReAnalysis = function( code ){
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "menu-analysis.cgi", { command:'', code:code, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Reanalysis' );
	});
};
