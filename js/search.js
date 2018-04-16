function displaySearchResults(results) {
  var searchResults = document.getElementById('search-results');

  if (results.length) { // Are there any results?
    var appendString = '';

    for (var i = 0; i < results.length; i++) {  // Iterate over the results

      appendString += ' <div class="hr-line-dashed"></div>';
      appendString += '          <div class="search-result">';
      appendString +=           '<a href="' + results[i].url + '"><h3>' + results[i].title + '</h3></a>';
      appendString += '                      <p>';
      appendString += results[i].content.substring(0, 300);
      appendString += '...                      </p>';
      appendString += '                  </div>';
      appendString += '                  <div class="hr-line-dashed"></div>';

    }

    searchResults.innerHTML = appendString;
  }

}

var options = {
  shouldSort: true,
  threshold: 0.6,
  location: 0,
  distance: 100,
  maxPatternLength: 32,
  minMatchCharLength: 2,
  keys: [{
     name: 'title',
     weight: 0.9
   }, {
     name: 'content',
     weight: 0.1
   }]
};

var fuse = new Fuse(list_site, options);

function RunSearch(item){
  var results = fuse.search(item);
  displaySearchResults(results);
}
