from pickle import dump, load
from os.path import exists
import codecs

min_length = 4
max_length = 12

ideal_length = 4
length_influence = 0.25

first_letters = "CEFGKRS"
other_letters = "cefgrskya"

prefix = ""
suffix = ""

cutoff_score = 0.3

word_lists = {
    "English": "WordsEn",
    "Danish": "WordsDan",
    "Dutch":   "WordsNld",
    "Swahili": "swahili",
    "Yiddish": "yiddish",
    "Japanese": "japanese",
    "Tolkien": "tolkien",
    "Rock Groups": "rock-groups",
    "Music Classical": "music-classical",
    "Music Country": "music-country",
    "Music Jazz": "music-jazz",
    "Movie Characters": "movie-characters",
}

selected_word_list = "English"



class FontNameGenerator:

    def __init__(self, word_lists, word_list, min_length, max_length, ideal_length, length_influence, first_letters, other_letters, prefix, suffix, cutoff_score):
        self.word_lists = word_lists
        self.word_list = word_list # Name
        self.min_length = min_length
        self.max_length = max_length
        self.ideal_length = ideal_length
        self.length_influence = length_influence
        self.first_letters = first_letters
        self.other_letters = other_letters
        self.prefix = prefix
        self.suffix = suffix
        self.cutoff_score = cutoff_score

    @property
    def word_list(self):
        return self._word_list

    @word_list.setter
    def word_list(self, value):
        # Set word list by name
        if value in self.word_lists:
            self.word_list_filename = self.word_lists[value]
            self._word_list = self.load_wordlist()
        else:
            print("Unknown word list: %s" % value)

    @property
    def selected_word_list(self):
        return self._word_list_filename

    @selected_word_list.setter
    def selected_word_list(self, value):
        self._selected_word_list = value
        self.word_list_filename = self.word_lists[sorted(self.word_lists.keys())[self._selected_word_list]]
        self.word_list = self.load_wordlist()

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value.strip()
        if self._prefix:
            self._prefix += " "

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self._suffix = value.strip()
        if self._suffix:
            self._suffix = " " + self._suffix


    def write_txt(self, the_dict):
        f = codecs.open("found_names.txt", "wb", "utf-8")
        for s in sorted(the_dict.keys(), reverse=True):
            if s > cutoff_score:
                f.write("\n****** Score: %s ******\n" % s)
                for w, r, d in sorted(the_dict[s]):
                    f.write("%s%s%s%s\n" % (prefix, w[0].upper(), w[1:], suffix))
            else:
                break
        f.close()


    def write_csv(self, the_dict):
        f = codecs.open("found_names.csv", "wb", "utf-8")
        f.write('"Name";"Score";"Letter Uniqueness";"Length Score"\n')
        for s in sorted(the_dict.keys(), reverse=True):
            if s > 0.5:
                for w, r, d in sorted(the_dict[s]):
                    f.write(
                        '"%s%s%s%s";"%s";"%s";"%s"\n' % (
                            prefix,
                            w[0].upper(),
                            w[1:],
                            suffix,
                            int(round(s, 1) * 10),
                            int(round(r, 1) * 10),
                            int(round(d, 1) * 10),
                        )
                    )
            else:
                break
        f.close()


    def load_wordlist(self):
        if not exists("%s.pickle" % self.word_list_filename):
            with codecs.open("%s.txt" % self.word_list_filename, "rb", "utf-8") as txt_file:
                self.words = [line.strip() for line in txt_file]
            with open("%s.pickle" % self.word_list_filename, "wb") as pickle_file:
                dump(self.words, pickle_file)
        else:
            with open("%s.pickle" % self.word_list_filename, "rb") as f:
                self.words = load(f)


    def get_diff_score(self, word):
        deviation_score = 1.0
        diff = len(word) - int(self.ideal_length)
        #print("Diff:", diff)
        if diff < 0:
            #print(diff, ideal_length, min_length)
            deviation_score = 1 - self.length_influence * float(abs(diff)) / (int(self.ideal_length) - int(self.min_length))
        elif diff > 0:
            #print(diff, max_length, ideal_length)
            deviation_score = 1 - self.length_influence * float(abs(diff)) / (int(self.max_length) - int(self.ideal_length))
        return deviation_score


    def get_filtered_words(self):        
        filtered_words = {}

        for w in self.words:
            if int(self.min_length) <= len(w) <= int(self.max_length):
                #print("\n", w)
                score = 0.0
                for l in w[1:]:
                    if l in self.other_letters:
                        score += 1
                #print("Score:", score)
                repetition = (1 + len(set(list(w))) / float(len(w))) / 2
                #print("Repetition:", repetition)
                score = score / len(w)
                score = repetition * score
                deviation = self.get_diff_score(w)
                score = deviation * score
                #print("Adjust score:", score)
                if w[0].upper() in self.first_letters:
                    score *= 2
                #print("Adjust score:", score)
                score = round(score, 2)
                if score in filtered_words:
                    #filtered_words[score].append("%s (%0.1f)" % (w, repetition))
                    filtered_words[score].append((w, repetition, deviation))
                else:
                    #filtered_words[score] = ["%s (%0.1f)" % (w, repetition)]
                    filtered_words[score] = [(w, repetition, deviation)]
        final_words = {score: words for score, words in filtered_words.items() if score > self.cutoff_score}
        return self.prefix, self.suffix, final_words

if __name__ == "__main__":
    fng = FontNameGenerator(word_lists, selected_word_list, min_length, max_length, ideal_length, length_influence, first_letters, other_letters, prefix, suffix, cutoff_score)
    print(fng.get_filtered_words())
    #draw_words(filtered_words)
    # Write results to file
    #write_csv(filtered_words)
    #write_txt(filtered_words)
