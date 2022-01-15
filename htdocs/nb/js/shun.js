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
