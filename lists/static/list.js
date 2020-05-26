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
window.Supertodolists.initialize = function(){
	// console.log('AAAA')
	// debugger;
	$('input[name="text"]').val('')
	$('input[name="text"]').on('keypress', function () {
	  $('.show-errors').hide();
	});
};