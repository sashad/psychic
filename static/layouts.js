function waitCounter ( counter ) {
    if ( counter > 0 ) {
        setTimeout(() => {
            waitCounter ( counter );
        }, 25);
    }
}

function isScriptLoaded (src) {
    return document.querySelector('script[src="' + src + '"]');
}

var htmlLoadedCount = 0; //если загружаются скрипты, то им надо дождаться загрузки HTML объектов

function loadScript (scriptName, reload=false) {

    //waitCounter(htmlLoadedCount); // Ожидаем загрузки HTML объектов! плохой метод, пусть будет но пока не будем использовать
    
    var script = isScriptLoaded(scriptName); 
    if (Boolean(script)) {
        if (reload) {
            console.log("!-------------- script:", script);
            script.parentNode.removeChild(script)
        } else {
            return;
        }
    }

    // Create new script element
    const app = document.createElement('script');
    app.src = scriptName;
    
    // Append to the `head` element
    app.addEventListener('load', function(e) {
        console.log("!--- Script loaded ---!", e);
        // The script is loaded completely
        // Do something
    });
    document.head.appendChild(app);
}

function ajaxLoadScript (base, params=null, reload=false) {
    webix.ajax().get(base + "/get_scripts", params, {
		error:function(text, params, XmlHttpRequest){
			console.log("Error ajaxLoadScript:", text, data, XmlHttpRequest);
		},
		success:function(text, data, XmlHttpRequest){
		    let scripts = JSON.parse(text);
		    if (!(scripts instanceof Array)) return;
			scripts.forEach ( function (scr, index) {
			    loadScript (base + '/' + scr, reload);
			});
		}
	});
}

function isCSSLoaded (src) {
    return document.querySelector('link[href="' + src + '"]');
}

function loadCSS (cssName, reload=false) {
    var css = isCSSLoaded(cssName); 
    if (Boolean(css)) {
        if (reload) {
            console.log("!-------------- CSS:", css);
            css.parentNode.removeChild(css)
        } else {
            return;
        }
    }

    // Create new link css element
    const link = document.createElement('link');
    link.href = cssName;
    link.rel = "stylesheet";
    
    // Append to the `head` element
    link.addEventListener('load', function(e) {
        console.log("!--- css loaded ---!", e);
        // The script is loaded completely
        // Do something
    });
    document.head.appendChild(link);
}

function isHTMLLoaded (src) {
    return document.querySelector('div[source="' + src + '"]');
}

function loadHTML (htmlName, func=null, reload=false, params=null ) {
    var html = isHTMLLoaded(htmlName); 
    if (Boolean(html)) {
        if (reload) {
            console.log("!-------------- HTML:", html);
            html.parentNode.removeChild(html)
        } else {
            return;
        }
    }

    // Create new link css element
    var div = document.createElement('div');
    div.setAttribute('source', htmlName);
    div.classList.add("invisible");
    console.log("!-------------- div:", div);
/*    
    // Append to the `head` element
    div.addEventListener('load', function(e) {
        console.log("!--- html loaded ---!", e);
        // The script is loaded completely
        // Do something
    });
*/
    htmlLoadedCount++;
    webix.ajax().get(htmlName, params, {
		error:function(text, params, XmlHttpRequest){
            htmlLoadedCount--;
			console.log("Error ajaxLoadScript:", text, data, XmlHttpRequest);
		},
		success:function(text, data, XmlHttpRequest){
		    div.innerHTML = text;
            document.body.appendChild(div);
            htmlLoadedCount--;
            console.log("!--- html loaded ---!", div);
            if (typeof func === 'function') {
                func();
            }
		}
	});
}

var baseAppPath = 'static';
var sessionData = null;

webix.ready( function() {
    console.log('Wegix ready!');
    webix.ajax().get('sessionData', null, {
		error:function(text, data, XmlHttpRequest){
			console.log("Error sessionData:", text, data, XmlHttpRequest);
		},
		success:function(text, data) {
		    sessionData = JSON.parse(text);
            // Create new script element
            loadScript (baseAppPath + '/app.js');
		}
	});
});
