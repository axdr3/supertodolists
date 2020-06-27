// The QUnit.test function defines a test case, a bit like def
// test_something(self) did in Python.  Its first argument is a name for the
// test, and the second is a function for the body of the test.

// 	The assert.equal function is an assertion; very much like assertEqual,
// it compares two arguments. Unlike in Python, though, the message is displayed
// both for failures and for passes, so it should be phrased as a positive
// rather than a negative.

// The jQuery .trigger method is mainly used for testing.
// It says "fire off a JavScript DOM event on the element(s)".
// Here we use the keypress event, which is fired off by the
// browser behind the scenes whenever a user types something into a particular
// input element. We explicitly declare an object as a property of the
// "window" global,
// giving it a name that we think no one else is likely to use.

window.Supertodolists = {};

window.Supertodolists.updateItems = function (url) {
	
  $.get(url).done(function (response) {
    if (!response.items) {return;}
    var rows = '';
    for (var i=0; i<response.items.length; i++) {
      var item = response.items[i];
      rows += '\n<tr><td>' + (i+1) + ': ' + item.text + '</td></tr>';
    }
    $('#id_list_table').html(rows);
    console.log('rows' + rows)
  });
};

window.Supertodolists.initialize = function(params){

	$('input[name="text"]').on('keypress', function () {
	  $('.show-errors').hide();
	});

	if (params) {
		window.Supertodolists.updateItems(params.listApiUrl);
	    var form = $('#id_item_form');
		form.on('submit', function(event) {
		    event.preventDefault();
		    $.post(params.itemsApiUrl, {
		    	'list': params.listId,
				'text': form.find('input[name="text"]').val(),
			    'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val(),
			    // 'error': form.find('error')
			}).done(function() {
				$('.show-errors').hide();

				window.Supertodolists.updateItems(params.listApiUrl);
			})
			.fail((xhr) => {
				$('.show-errors').show();
		        if (xhr.responseJSON) {
		          $('.show-errors .help-block').text(xhr.responseJSON.error || xhr.responseJSON.non_field_errors);
		        } else {
		          $('.show-errors .help-block').text('Error talking to server. Please try again.');
		        }
			});
		});
	}
};