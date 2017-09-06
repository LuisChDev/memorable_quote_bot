# memorable\_quote_bot
This bot was inspired by my favorite [Abraham Lincoln quote](https://www.askideas.com/wp-content/uploads/2016/11/The-problem-with-quotes-found-on-the-Internet-is-that-they-are-often-not-true.-Abraham-Lincoln.jpg), and of course, on [trippin' through time](http://reddit.com/r/trippinthroughtime) style humor. I hope it does not disrupt the regular course of discussion on Reddit.

So here's a little summary of what the bot does:

* starts by fetching the forbidden subreddits from a file
* then it fetches the latest comments from /all
* it matches it against the regex (which aims for medium-sized non-nested quotes)
* also it checks whether the subreddit the comment comes from has banned the bot
* if it matches, isn't banned, and the comment hasn't been replied to yet:
   * the comment is added to the list
   * build_image is called (see below) with the match and the comment's id
   * the comment is replied to

**the** image is built in the following way:

* after being called, it creates an empty image
* it then selects a random image + signature combo from the archive
* based on the image's dimensions it calculates the offset so they are centered (they were prepared beforehand to always fit in the spot)
* the image is pasted together with the signature
* then a font is selected for the quote
TODO: make sure this font is the same one as the one in the signatures.
* a draw object is created and used to write the quote. textwrap is used to ensure the lines fit inside their spot.
* all is wrapped up, and the image is saved temporarily, uploaded to imgur, and
then the function returns the url of the image.

**I** included a script to automate the reduction of images and the generation of
signatures. to use it, run it in the terminal, and when prompted:
* type 'sigs' to generate again the signatures from the file.
* type 'addpic' and input the directory of the image and the name of the person to add them.
* type 'removepic' and the name to remove their names and pictures from the list.
