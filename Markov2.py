import string
import random
import twitter
import re

api = twitter.Api(consumer_key='EDcqtmY6rAl3dC98K9GfTODR6',
      consumer_secret='vwbjFTnC9MPYf05RHN14AsAOrNTCX19rKx57UoHZG7OIl84bhN',
      access_token_key='888372950184869890-1UCsUYXkG4yaFbkX4gHZSE5kFQUrNMr',
      access_token_secret='fDReVF4dzPjHjQDS4iRGKvSDuoQXGGZWU0Xc5piGJQ14f')

def twitter1(screen_name):
    """
    Extracts tweets from a user assigned and stores it into a txt file.
    RT, hashtags and url are stripped away.

    screen_name: twitter username
    return: txt file of the tweets in the whole timeline
    """
    t = api.GetUserTimeline(screen_name="%s" %screen_name, count=500)
    tweets = [i.AsDict() for i in t]

    twts = ""
    for t in tweets:
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",t['text']).split())
        twts += text +" "
#        print(text)

    f = open('tweetextracted.txt','w')
    f.write(screen_name +  '\n' * 2 + twts)
    f.close()


class Markov(object):

    def __init__(self, order=2, n=100):
        """
        suffix map is a dictionary with every two consecutive word,
        which is prefix, as key and the third one as value
        so that when you  map what a third word could
        be based on the two previous words

        Order being two indicates that it looks at two consecutive word
        to generate next word
        """
        self.suffix_map = {}
        self.prefix = ()
        self.order = int(order)  # order ot words prefix
        self.n = int(n)  # numbers of words to generate

    def process_word(self, word):
        """Processes each word.

        word: string
        order: integer

        During the first few iterations, all we do is store up the words;
        after that we start adding entries to the dictionary.
        """

        if len(self.prefix) < self.order:
            self.prefix += (word,)
            return  # store up the workds for first few iteration

        try:
            self.suffix_map[self.prefix].append(word)
        except KeyError:
            # if there is no entry for this self.prefix, make one
            self.suffix_map[self.prefix] = [word]

        self.prefix = shift(self.prefix, word)

    def random_text(self):
        """Generates random words from the analyzed text.
        Starts with a random prefix from the dictionary.

        n: number of words to generate
        """
        start = random.choice(list(self.suffix_map.keys()))

        words = ''
        for i in range(self.n):
            suffixes = self.suffix_map.get(start, None)
            if suffixes is None:
                # if the start isn't in map, we got to the end of the
                # original text, so we have to start again.
                self.n = self.n - i
                self.random_text()
                return

            word = random.choice(suffixes)
            words = words + word + " "
            start = shift(start, word)
        with open("Generated.txt", "w") as output:
            output.write(str(words))


def get_word_list(file_name, markov_obj):
    """

    Header comments, punctuation, and whitespace are stripped away. The function
    returns a list of the words used in the book as a list. All words are
    converted to lower case.
        -> process_file loops through the lines of the file, passing them to
    process_line
    """

    fp = open(file_name)

    for line in fp:
        for word in line.split():
            word = word.strip(string.punctuation + string.whitespace)
            word = word.lower()
            markov_obj.process_word(word)


def shift(t, word):
    """Forms a new tuple by removing the head and adding word to the tail.
    t: tuple of strings
    word: string
    Returns: tuple of strings
    """
    return t[1:] + (word,)


def main(filename='', n=100, order=2, *args):
    """
    Main function of the code

    :param filename: name of the txt file
    :param n: number of words printed as a result
    :param order: number of words prior to generate the next word
    :return: new texts generated after analyzing the text collected from the twitter

    """
    try:
        n = int(n)
        order = int(order)
    except ValueError:  # right type but wrong value
        print('ValueError')
    else:
        markov_obj = Markov(order, n)
        get_word_list(filename, markov_obj)
        markov_obj.random_text()

if __name__ == '__main__':
    twitter1("BarakObama")
    main(filename='tweetextracted.txt', n=50, order=2)
