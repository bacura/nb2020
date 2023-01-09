//shun.js ver 0.00b (2023/01/08)

/////////////////////////////////////////////////////////////////////////////////
// Cooking school //////////////////////////////////////////////////////////////

//
var initSchool = function(){
	flashBW();
	$.post( "school.cgi", { command:"menu" }, function( data ){
		$( "#LINE" ).html( data );
		dline = true;
		displayBW();
	});
	$.post( "school.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );
		dl1 = true;
		displayBW();
	});
};

// School koyomi change
var changeSchoolk = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "school.cgi", { command:"init", yyyy_mm:yyyy_mm }, function( data ){ $( "#L1" ).html( data );});
};

// School status change
var changeSchoolkSt = function( dd, ampm, status ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "school.cgi", { command:"changest", yyyy_mm:yyyy_mm, dd:dd, ampm:ampm, status:status }, function( data ){ $( "#L1" ).html( data );});
};

// School open
var openSchoolk = function( dd, ampm ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "school.cgi", { command:"open", yyyy_mm:yyyy_mm, dd:dd, ampm:ampm }, function( data ){ $( "#L1" ).html( data );});
};

/////////////////////////////////////////////////////////////////////////////////
// Cooking school menu //////////////////////////////////////////////////////////////

// menu
var initSchoolMenu = function(){
	$.post( "school-menu.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data );});
};

// Making new school menu label group
var mekeSchoolGroup = function(){
	var group_new = document.getElementById( 'group_new' ).value;
	if( group_new != '' ){
		$.post( "school-menu.cgi", { command:"group_new", group_new:group_new }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( 'Group name! (>_<)' );
	}
};

// Deleting school menu label group
var delSchoolGroup = function( label_group ){
	if(document.getElementById( "del_check_" + label_group ).checked){
		$.post( "school-menu.cgi", { command:"group_del", group_new:label_group }, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( label_group );
		});
	}else{
		displayVIDEO( 'Check! (>_<)' );
	}
};

// Changing school menu label
var changeSchoolLabel = function( label_group, group_no, label_no ){
	var label_new = document.getElementById( 'label' + group_no + '_' + label_no ).value;
	$.post( "school-menu.cgi", { command:"label_change", label_group:label_group, label_no:label_no, label_new:label_new }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( label_new );
	});
};

// Select school menu selector
var selectSchoolMenu = function(){
	var group_select = document.getElementById( 'group_select' ).value;
	var label_select = document.getElementById( 'label_select' ).value;
	var month_select = document.getElementById( 'month_select' ).value;
	var week_select = document.getElementById( 'week_select' ).value;
	$.post( "school-menu.cgi", { command:'menu_select', group_select:group_select, label_select:label_select, month_select:month_select, week_select:week_select }, function( data ){ $( "#L1" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Cooking school stock //////////////////////////////////////////////////////////////

// menu
var initSchoolStock = function(){
	$.post( "school-stock.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dline = true;
		dl1 = true;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Cooking school custom //////////////////////////////////////////////////////////////

// custom
var initSchoolCustom = function(){
	$.post( "school-custom.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dline = true;
		dl1 = true;
		displayBW();
	});
};

// Update school code
var saveSchoolCustom = function(){
	var cs_code = document.getElementById( 'cs_code' ).value;
	var cs_name = document.getElementById( 'cs_name' ).value;
	var format = 0;
displayVIDEO( cs_name );
	if( document.getElementById( 'enable0' ).checked ){ var enable0 = 1; }else{ var enable0 = 0; }
	if( document.getElementById( 'enable1' ).checked ){ var enable1 = 1; }else{ var enable1 = 0; }
	if( document.getElementById( 'enable2' ).checked ){ var enable2 = 1; }else{ var enable2 = 0; }
	if( document.getElementById( 'enable3' ).checked ){ var enable3 = 1; }else{ var enable3 = 0; }
	var title0 = document.getElementById( 'title0' ).value;
	var title1 = document.getElementById( 'title1' ).value;
	var title2 = document.getElementById( 'title2' ).value;
	var title3 = document.getElementById( 'title3' ).value;
	var menu_group0 = document.getElementById( 'menu_group0' ).value;
	var menu_group1 = document.getElementById( 'menu_group1' ).value;
	var menu_group2 = document.getElementById( 'menu_group2' ).value;
	var menu_group3 = document.getElementById( 'menu_group3' ).value;
	var document0 = document.getElementById( 'document0' ).value;
	var document1 = document.getElementById( 'document1' ).value;
	var document2 = document.getElementById( 'document2' ).value;
	var document3 = document.getElementById( 'document3' ).value;
	var print_ins = document.getElementById( 'print_ins' ).value;
	var qr_ins = document.getElementById( 'qr_ins' ).value;

	$.post( "school-custom.cgi", { command:"save", cs_code:cs_code, cs_name:cs_name, format:format,
		enable0:enable0, enable1:enable1, enable2:enable2, enable3:enable3,
		title0:title0, title1:title1, title2:title2, title3:title3,
		menu_group0:menu_group0, menu_group1:menu_group1, menu_group2:menu_group2, menu_group3:menu_group3,
		document0:document0, document1:document1, document2:document2, document3:document3,
		print_ins:print_ins, qr_ins:qr_ins
	}, function( data ){ $( "#L1" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Management of account M //////////////////////////////////////////////////////////////

// Account list
var initAccountM = function(){
	$.post( "account-mom.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};


// New account form
var newAccountM = function(){
	$.post( "account-mom.cgi", { command:"new" }, function( data ){ $( "#L1" ).html( data );});
};


// Save new account
var saveAccountM = function(){
	var uid_d = document.getElementById( 'uid_d' ).value;
	var mail_d = document.getElementById( 'mail_d' ).value;
	var pass_d = document.getElementById( 'pass_d' ).value;
	var aliasu_d = document.getElementById( 'aliasu_d' ).value;
	var language_d = document.getElementById( 'language_d' ).value;
	$.post( "account-mom.cgi", { command:"save", uid_d:uid_d, mail_d:mail_d, pass_d:pass_d, aliasu_d:aliasu_d, language_d:language_d }, function( data ){ $( "#L1" ).html( data );});
};


// Update account
var updateAccountM = function( uid_d ){
	var mail_d = document.getElementById( 'mail_d' ).value;
	var pass_d = document.getElementById( 'pass_d' ).value;
	var aliasu_d = document.getElementById( 'aliasu_d' ).value;
	var language_d = document.getElementById( 'language_d' ).value;
	$.post( "account-mom.cgi", { command:"update", uid_d:uid_d, mail_d:mail_d, pass_d:pass_d, aliasu_d:aliasu_d, language_d:language_d }, function( data ){ $( "#L1" ).html( data );});
};


// Edit account
var editAccountM = function( uid_d ){
	$.post( "account-mom.cgi", { command:"edit", uid_d:uid_d }, function( data ){ $( "#L1" ).html( data );});
};


// Delete account
var deleteAccountM = function( uid_d ){
	if(document.getElementById( "delete_checkM" ).checked){
		$.post( "account-mom.cgi", { command:"delete", uid_d:uid_d }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( 'Check! (>_<)' );
	}
};


// Switch account
var switchAccountM = function( switch_id, uid_d ){
	if(document.getElementById( switch_id ).checked){ var switch_d = 1; }else{ var switch_d = 0; }
	$.post( "account-mom.cgi", { command:"switch", uid_d:uid_d, switch_d:switch_d }, function( data ){});
};


/////////////////////////////////////////////////////////////////////////////////
// Tokei R //////////////////////////////////////////////////////////////

// Tokei R init
var initToker = function(){
	flashBW();
	$.post( "toker.cgi", { mod:'line' }, function( data ){
		$( "#LINE" ).html( data );
		dline = true;
		displayBW();
	});
	$.post( "toker.cgi", { mod:'' }, function( data ){
		$( "#L1" ).html( data );
		dl1 = true;
		displayBW();
	});
};

var tokerForm = function( mod ){
	$.post( "toker.cgi", { mod:mod, command:'form' }, function( data ){ $( "#L1" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Nutrition visionnerz //////////////////////////////////////////////////////////////

// Init
var visionnerz = function( yyyymmdd ){
	$.post( "visionnerz.cgi", { command:'init', yyyymmdd:yyyymmdd }, function( data ){
		$( "#L4" ).html( data );

		$.post( "visionnerz.cgi", { command:'raw', yyyymmdd:yyyymmdd }, function( raw ){
			$( "#LF" ).html( raw );

			var column = ( String( raw )).split( ':' );
			var hours = ( String( column[0] )).split(',');
			var d_protein = ( String( column[1] )).split(',');
			var d_protein_ = ( String( column[2] )).split(',');
			var d_fat = ( String( column[3] )).split(',');
			var d_fat_ = ( String( column[4] )).split(',');
			var d_sugars = ( String( column[5] )).split(',');
			var d_sugars_ = ( String( column[6] )).split(',');
			var d_sodium = ( String( column[7] )).split(',');
			var d_potassium = ( String( column[8] )).split(',');
			var d_fiber = ( String( column[9] )).split(',');
			var d_water = ( String( column[10] )).split(',');
			var d_alcohol = ( String( column[11] )).split(',');

			var chart = c3.generate({
				bindto: '#visionnerz-intake',

				data: {
					x: '時間',
					axes: { '水分(g)':'y2', 'ナトリウム(mg)':'y2', 'カリウム(mg)':'y2' },
					columns: [hours, d_protein, d_fat, d_sugars, d_sodium, d_potassium, d_fiber, d_water, d_alcohol]
				},
				axis: {
					x: {
						 label:{text:'時間（時）', position:'outer-center' },
						 tick:{ values: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']}
					},
					y: {
			    		type:'linear', min:0, padding:{bottom:0},
			    		tick:{  values:['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'] },
	 					label:{ text:'たんぱく質 / 脂質 / 糖質 / 食物繊維 / アルコール', position: 'outer-middle' }
					},
					y2: {
						show: true,
			    		type: 'linear', min: 0, padding: {bottom: 0},
			    		tick: { format: d3.format( "01d" ) },
	 					label: { text: '水分 / ナトリウム / カリウム', position: 'outer-middle' }
					}
				},
				point: { show: false },
				legend: { show: true, position: 'right' }
			});
		});

		pushBW();
		flashBW();
		dll = true;
		dl4 = true;
		dlf = true;
		displayBW();
	});
};

//				data: {
//					columns: [ minutes, d_energy, d_protein, d_fat, d_carbohydrate, d_fiber, d_sodium ],
//					x: 'minutes',
//					axes: {
//						#{l['data_bfr']}: 'y2',
//					},
//					labels: false,
//					type : 'line',
//					colors: {
//						#{l['data_weight']}: '#dc143c',
//						#{l['data_bfr']}: '#228b22'
//					},
//				},
//
//				axis: {
//			    	x: {
//			    		type: 'timeseries',
//			    		tick: { culling:true }
//					},
//					y: {
//			    		type: 'linear',
//						padding: {top: 100, bottom: 200 },
//						label: { text: '#{l['label_weight']}', position: 'outer-middle' }
//					}
//					y2: {
//						show: true,
//			    		type: 'linear',
//						padding: {top: 200, bottom: 100},
//	 					tick: { format: d3.format("01d") },
//	 					label: { text: '#{l['label_bfr']}', position: 'outer-middle' }
//					}
//				},
//
//				legend: { show: true, position: 'bottom' },
//
//				line: { connectNull: true, step: { type: 'step' }},
//				zoom: { enabled: true, type: 'drag' },
//			});
//
//	//--------------------------------------------------------------------------
//			var chart_sub = c3.generate({
//				bindto: '#visionnerz-blood',
//
//				data: {
//					columns: [
//						f_weight,
//						f_bfr,
//						r_weight,
//						r_bfr,
//						p_weight,
//						p_bfr,
//						rd_weight,
//						rd_bfr
//					],
//					xs: { #{l['data_first']}:'f_bfr', #{l['data_latest']}:'rd_bfr', #{l['data_recent']}:'p_bfr', #{l['data_past']}:'r_bfr' },
//					labels: true,
//					type : 'scatter',
//					colors: { #{l['data_first']}:'#4b0082', #{l['data_latest']}:'#dc143c', #{l['data_recent']}:'#00ff00', #{l['data_past']}:'#c0c0c0'}
//				},
//
//				axis: {
//			    	x: {
//						label: { text: '#{l['label_bfr']}', position: 'outer-center' },
//						padding: {left: 1, right: 1 },
//						tick: { fit: false }
//					},
//					y: {
//						label: { text: '#{l['label_weight']}', position: 'outer-middle' },
//						padding: {top: 20, bottom: 20 },
//						tick: { fit: false }
//					},
//				},
//				grid: {
//	     			x: { show: true },
//	        		y: { show: true }
//	            },
//				legend: { show: true, position: 'bottom' },
//				point: { show: true, r: 4 },
//				tooltip: { show: false }
//			});
//
//			var menergy = column[9];
//			document.getElementById( 'menergy' ).value = menergy;
//		});
//
//	};
//
//	drawChart();
//
//
//

/////////////////////////////////////////////////////////////////////////////////
// Detective ////////////////////////////////////////////////////////////////////////

//
var initDetective = function(){
	var code = document.getElementById( "words" ).value;

	$.post( "detective.cgi", { command:'hints', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

//
var reasoning = function(){
	var volume = document.getElementById( "volume" ).value;
	var energy = document.getElementById( "energy" ).value;
	var protein = document.getElementById( "protein" ).value;
	var fat = document.getElementById( "fat" ).value;
	var carbo = document.getElementById( "carbo" ).value;
	var salt = document.getElementById( "salt" ).value;

	if(volume != '' && volume != '0' ){
		$.post( "detective.cgi", { command:'wait', volume:volume, energy:energy, protein:protein, fat:fat, carbo:carbo, salt:salt }, function( data ){
			$( "#L2" ).html( data );

			$.post( "detective.cgi", { command:'reasoning', volume:volume, energy:energy, protein:protein, fat:fat, carbo:carbo, salt:salt }, function( data ){
				$( "#L2" ).html( data );
			});
		});
	}else{
		displayVIDEO( 'Volume!(>_<)' );
	}
};

//
var detectiveAdopt = function( food_nos_solid, fw_ex_solid ){
	$.post( "detective.cgi", { command:'adopt', food_nos_solid:food_nos_solid, fw_ex_solid:fw_ex_solid }, function( data ){
//		$( "#L2" ).html( data );
		$.post( "cboard.cgi", { command:'init' }, function( data ){
			$( "#L1" ).html( data );
		});

		dl2 = false;
		displayBW();
	});
};

//
var loadDetectiveResult = function(){
	$.post( "detective.cgi", { command:'load_result' }, function( data ){ $( "#L2" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// 3D recipe plott search //////////////////////////////////////////////////////////////

// Dosplaying recipe by scatter plott
var recipe3ds = function(){
	flashBW();
	$.post( "recipe3ds.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );
		$.post( "recipe3ds.cgi", { command:'plott_area' }, function( data ){
			$( "#L2" ).html( data );
			recipe3dsPlottDraw();
			dl1 = true;
			dl2 = true;
			dl3 = true;
			displayBW();
		});
	});
};

// Dosplaying recipe by scatter plott
var recipe3dsPlottDraw = function(){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;

	var xitem = document.getElementById( "xitem" ).value;
	var yitem = document.getElementById( "yitem" ).value;
	var zitem = document.getElementById( "zitem" ).value;
	var zml = document.getElementById( "zml" ).value;
	var zrange = document.getElementById( "zrange" ).value;
	$.post( "recipe3ds.cgi", { command:'monitor', range:range, type:type, role:role, tech:tech, time:time, cost:cost,
		xitem:xitem, yitem:yitem, zitem:zitem, zml:zml, zrange:zrange }, function( data ){
		$( "#L3" ).html( data );
	});

	$.post( "recipe3ds.cgi", { command:'plott_data', range:range, type:type, role:role, tech:tech, time:time, cost:cost,
		xitem:xitem, yitem:yitem, zitem:zitem, zml:zml, zrange:zrange }, function( raw ){
		var column = ( String( raw )).split( ':' );
		var x_values = ( String( column[0] )).split(',');
		var y_values = ( String( column[1] )).split(',');
		var names = ( String( column[2] )).split(',');
		var codes = ( String( column[3] )).split(',');
		var x_tickv = ( String( column[4] )).split(',');

		var plott_size = document.documentElement.clientWidth
		if ( plott_size > 800 ){ var plott_size = plott_size * 0.9; }
		if ( plott_size > 1000 ){ var plott_size = plott_size * 0.9; }
		if ( plott_size > 1200 ){ var plott_size = plott_size * 0.9; }
		if ( plott_size > 1600 ){ var plott_size = plott_size * 0.9; }


		if ( chart != null ){
			chart.destroy();
			displayVIDEO( 'Flush!' );
		}

		var chart = c3.generate({
			bindto: '#recipe3ds_plott',
			size:{ width: plott_size, height: plott_size },

			data: {
				columns: [
					x_values,	// x軸
					y_values,	// y軸
				],
			    x: x_values[0],
				type: 'scatter'
//				colors:{ x_values[0]: '#ff44FF' }
			},
			axis: {
			    x: {
			    	type: 'indexed',
			    	label: x_values[0],
			    	min:0,
					tick: {
						fit: true,
						count: 10,
						format: d3.format( "01d" ),
						values: x_tickv
					},
					padding: { left: 0, right: 10 }
				},
			    y: {
			    	label: y_values[0],
			    	type: 'linear',
			    	min: 0,
			  		padding: { top: 10, bottom: 0 }
			    }
			},
			point: {
				r: 8,
				focus: { expand: { r: 10 }}
			 },
			grid: {
     			x: { show: true },
        		y: { show: true }
            },
			legend: { show: false },
			tooltip: {
				grouped: false,
//				format: {
//					title: function ( x, index ) { return "[" + index + "]" + names[index]; },
//					name: function ( name, ratio, id, index ) { return x_values[0] + ' : ' + y_values[0]; },
//					value: function ( value, ratio, id, index ) { return x_values[index + 1] + ' : ' + y_values[index + 1];  }
//				}
				contents: function (d, defaultTitleFormat, defaultValueFormat, color) {
					var ix = d[0].index;
					var tooltip_html = '<table style="background-color:#ffffff; font-size:1.5em;">';
					tooltip_html += '<tr><td colspan="2"  style="background-color:mistyrose;">' + names[ix] + '</td></tr>'
					tooltip_html += '<tr><td>' + x_values[0] + '</td><td>: ' + x_values[ix + 1] + '</td></tr>'
					tooltip_html += '<tr><td>' + y_values[0] + '</td><td>: ' + y_values[ix + 1] + '</td></tr>'
					tooltip_html += '</table>'

					return tooltip_html;
				}
			},
			onclick: function ( d, element ){
				console.log( "onclick", d, i );
			}
		});
	});
};


// Dosplaying recipe by scatter plott
var recipe3dsReset = function(){
	document.getElementById( "range" ).value = 0;
	document.getElementById( "type" ).value = 99;
	document.getElementById( "role" ).value = 99;
	document.getElementById( "tech" ).value = 99;
	document.getElementById( "time" ).value = 99;
	document.getElementById( "cost" ).value = 99;

	document.getElementById( "xitem" ).value = 'ENERC';
	document.getElementById( "yitem" ).value = 'ENERC';

	document.getElementById( "zitem" ).value = 'ENERC';
	document.getElementById( "zml" ).value = 0;
	document.getElementById( "zrange" ).value = 0;
};


// Dosplaying recipe by scatter plott
var recipe3dsPlottDraw = function(){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;

	var xitem = document.getElementById( "xitem" ).value;
	var yitem = document.getElementById( "yitem" ).value;
	var zitem = document.getElementById( "zitem" ).value;
	var zml = document.getElementById( "zml" ).value;
	var zrange = document.getElementById( "zrange" ).value;
	$.post( "recipe3ds.cgi", { command:'monitor', range:range, type:type, role:role, tech:tech, time:time, cost:cost,
		xitem:xitem, yitem:yitem, zitem:zitem, zml:zml, zrange:zrange }, function( data ){
		$( "#L3" ).html( data );
	});

	$.post( "recipe3ds.cgi", { command:'plott_data', range:range, type:type, role:role, tech:tech, time:time, cost:cost,
		xitem:xitem, yitem:yitem, zitem:zitem, zml:zml, zrange:zrange }, function( raw ){
		var column = ( String( raw )).split( ':' );
		var x_values = ( String( column[0] )).split(',');
		var y_values = ( String( column[1] )).split(',');
		var names = ( String( column[2] )).split(',');
		var codes = ( String( column[3] )).split(',');
		var x_tickv = ( String( column[4] )).split(',');

		var plott_size = document.documentElement.clientWidth
		if ( plott_size > 800 ){ var plott_size = plott_size * 0.9; }
		if ( plott_size > 1000 ){ var plott_size = plott_size * 0.9; }
		if ( plott_size > 1200 ){ var plott_size = plott_size * 0.9; }
		if ( plott_size > 1600 ){ var plott_size = plott_size * 0.9; }


		if ( chart != null ){
			chart.destroy();
			displayVIDEO( 'Flush!' );
		}

		var chart = c3.generate({
			bindto: '#recipe3ds_plott',
			size:{ width: plott_size, height: plott_size },

			data: {
				columns: [
					x_values,	// x軸
					y_values,	// y軸
				],
			    x: x_values[0],
				type: 'scatter'
//				colors:{ x_values[0]: '#ff44FF' }
			},
			axis: {
			    x: {
			    	type: 'indexed',
			    	label: x_values[0],
			    	min:0,
					tick: {
						fit: true,
						count: 10,
						format: d3.format( "01d" ),
						values: x_tickv
					},
					padding: { left: 0, right: 10 }
				},
			    y: {
			    	label: y_values[0],
			    	type: 'linear',
			    	min: 0,
			  		padding: { top: 10, bottom: 0 }
			    }
			},
			point: {
				r: 8,
				focus: { expand: { r: 10 }}
			 },
			grid: {
     			x: { show: true },
        		y: { show: true }
            },
			legend: { show: false },
			tooltip: {
				grouped: false,
//				format: {
//					title: function ( x, index ) { return "[" + index + "]" + names[index]; },
//					name: function ( name, ratio, id, index ) { return x_values[0] + ' : ' + y_values[0]; },
//					value: function ( value, ratio, id, index ) { return x_values[index + 1] + ' : ' + y_values[index + 1];  }
//				}
				contents: function (d, defaultTitleFormat, defaultValueFormat, color) {
					var ix = d[0].index;
					var tooltip_html = '<table style="background-color:#ffffff; font-size:1.5em;">';
					tooltip_html += '<tr><td colspan="2"  style="background-color:mistyrose;">' + names[ix] + '</td></tr>'
					tooltip_html += '<tr><td>' + x_values[0] + '</td><td>: ' + x_values[ix + 1] + '</td></tr>'
					tooltip_html += '<tr><td>' + y_values[0] + '</td><td>: ' + y_values[ix + 1] + '</td></tr>'
					tooltip_html += '</table>'

					return tooltip_html;
				}
			},
			onclick: function ( d, element ){
				console.log( "onclick", d, i );
			}
		});
	});
};

/////////////////////////////////////////////////////////////////////////////////
// JSON edit //////////////////////////////////////////////////////////////

// JSON list init
var initJsonlist = function(){
	$.post( "json-list.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Media edit //////////////////////////////////////////////////////////////

// Media list init
var initMedialist = function(){
	$.post( "media-list.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};
