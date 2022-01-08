webix.ui({
    rows:[
        {
	        type: "header",
	        template: "Тестирование экстрасенсов",
	        borderless: true,
            css: "webix_dark", 
        },
        {
          //width: 700, 
          id: "FORM",
          view: "form",
          scroll: false,
          padding: 60,
          rows:[
            {
                template:"Загадайте число?",
                height: 26,
                borderless: true,
            },
            {
                id: "number",
                view: "text",
                label: "Число",
                name: "value",
                type: "number",
                width: "300",
                value: "",
                hidden: true,
            },
            { id: "button", view:"button", width: 200, align: "left", value:"Загадал", click:function() {
                let value = $$('number');
                let button = $$('button');
                let form = $$('FORM');
                let history = $$('history');
                if (value.config.hidden) {
                    value.show();
                    button.setValue("Сказать число");
                    form.refresh();
                    value.focus();
                    webix.ajax().get('guesses', {cmd: 'guess'}, {
                		error: function(text, data, XmlHttpRequest){
                			console.log("Errors :", text, data, XmlHttpRequest);
                		},
                		success:function(text, data) {
                		    let guess = JSON.parse(text);
                			console.log("Success :", guess);
                			history.clearAll();
                			history.load('history');
                		}
                	});
                } else {
                    webix.ajax().get('guesses', this.getParentView().getValues(), {
                		error: function(text, data, XmlHttpRequest){
                			console.log("Errors :", text, data, XmlHttpRequest);
                		},
                		success:function(text, data) {
                		    let guess = JSON.parse(text);
                		    if ( guess.error ) {
                                webix.message('Ошибка ввода данных!');
                		    } else {
                                value.setValue('');
                                value.hide();
                                button.setValue("Загадал");
                                form.refresh();
                    			console.log("Success :", guess);
                    			history.clearAll();
                    			history.load('history');
                		    }
                		}
                	});
                }
            }}
          ]
        },
        {
            id: "history",
            view: "datatable",
            autoConfig: true,
            columns: sessionData['histHeaders'],
            url: 'history',
            //data: [
            //    { id:1, user: "5", psych1: '6 / 0', psych2: '6 / 0', psych3: '6 / 0', psych4: '6 / 0'},
            //]
        }
    ]
});
