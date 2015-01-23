
function Occurence(word) {
    this.word = word;
    this.count = 1;
    var priv = function() {

    };
    
}


function Tuple() {
    this.words = {};
    this.list = [];
    this.totalCount = 0;
}

var AutoComplete = {
    data: {},
    generateKey: function(preWords) {
	var key = preWords.join("¤").toLowerCase();
	//console.log("added: ", key);
	return key;
    },
    addWord: function(prWords, word) {
	var preWords = prWords.slice(0);
	var key = this.generateKey(preWords);
	var tup = this.data[key];
	if (tup == null) {
	    tup = new Tuple();
	    this.data[key] = tup;
	}
	var occurence = null;
	if (_.has(tup.words, word)) {
	    occurence = tup.words[word];
	    occurence.count += 1;
	} else {
	    occurence = new Occurence(word); 
	    tup.words[word] = occurence;
	    tup.list.push(occurence);
	}
	
	tup.totalCount++;
    },

    sortOccurences: function() {
	_.each(this.data, function(tup) {
	    tup.list.sort(function(o1, o2) {
		return o2.count-o1.count;
	    });
	});
    },

    getWord: function(preWords) {
	if (preWords.length < 2) 
	    preWords = ["^"].concat(preWords);
	for (var i=0; i<preWords.length; i++) {
	    var pWords = preWords.slice(i, preWords.length);
	    var key = this.generateKey(pWords);
	    var tup = this.data[key];
	    if (tup == null) continue;
	    var count = Math.random()*tup.totalCount-1;
	    var index = 0;
	    while (count>0) {
		count -= tup.list[index].count;
		index++;
	    }
	    index = Math.min(index, tup.list.length-1);
	    console.log(index, tup.list.length);
	    //if (tup.list[index].word == "$")
		//return null;
	    return tup.list[index].word;
	}
    },

    parseText: function(text) {
	var ac = this;
	_.each(text, function(sentence, sindex) {
	    //if (sindex > 1000)
		//return;
	    sentence.push("$");
	    var preWords = ["^"];
	    _.each(sentence, function(word, index) {
		if (preWords.length>3) {
		    preWords = preWords.slice(1);
		}
		//console.log("sddf", preWords, word);

		for (var i=0; i<preWords.length; i++) {
		    var pWords = preWords.slice(i);
		    //console.log("-", pWords);
		    ac.addWord(pWords, word);
		}
		preWords.push(word);
	    });
	});
	this.sortOccurences();
    },
    generateSentence: function(startSentence) {
	var sentence = startSentence.slice(0);

	var search = startSentence.slice(Math.max(0, startSentence.length-3));
	for (var i=3; i<50; i++) {
	    var word = AutoComplete.getWord(search);
	    if (word == null)
		break;
	    sentence.push(word);
	    search = search.slice(1);
	    search.push(word);
	    //console.log(search);
	}
	return sentence;
	//console.log(sentence);
    }
};

/*var data = [
    ["This", "is", "a", "sentence", "which", "has", "lots", "of", "words"],
    ["some","strange","thing","that","doesn't","matter"],
    ["some","strange","thing","that","doesn't","matter"],
    ["this", "is", "a", "strange"],
    ["this", "is", "a", "strange"],
    ["strange", "lots"],
];*/


$(function() {
    //console.log(data);
    AutoComplete.parseText(data);
    //console.log(AutoComplete, AutoComplete.getWord(["^", "vi", "is"]));
    //console.log(AutoComplete.generateSentence(["vi", "kan"]));
    //console.log(AutoComplete.data);
});


function showResult() {
    var search = $("#search");
    var result = $("#result");
    var res = AutoComplete.generateSentence(search.val().split(" ")).join(" ");
    if (res.indexOf("$")!==-1)
	res = res.split("$")[0];
    result.text(res);
}
