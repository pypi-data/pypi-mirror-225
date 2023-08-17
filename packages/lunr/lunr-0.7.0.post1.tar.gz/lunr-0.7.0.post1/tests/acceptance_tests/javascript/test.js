const fs = require('fs')
const lunr = require('lunr')
require("lunr-languages/lunr.stemmer.support")(lunr);
require("lunr-languages/lunr.es")(lunr);

const data = JSON.parse(
  fs.readFileSync('./../fixtures/lang_es.json'))
let documents = {}
const idx = lunr(function () {
  this.use(lunr.es)
  this.field('title')
  this.field('text')
  this.ref('id')
  for (doc of data.docs) {
    this.add(doc)
    documents[doc.id] = doc
  }
})

console.log('-----------')

let results = idx.search(process.argv[2])

console.log('-----------')
for (result of results) {
  let doc = documents[result.ref]
  console.log(`${result.ref} "${doc.title}" [${result.score}]\n`)
}
