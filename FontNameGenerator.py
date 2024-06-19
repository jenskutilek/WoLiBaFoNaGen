import codecs
import sys
from pathlib import Path

min_length = 4
max_length = 12

ideal_length = 4
length_influence = 0.25

first_letters = "CEFGKRS"
other_letters = "cefgrskya"

name_prefix = ""
name_suffix = ""

cutoff_score = 0.3

word_lists = {
    "English": "wordsEn",
    "Danish": "wordsDan",
    "Dutch": "wordsNld",
    "Swahili": "swahili",
    "Yiddish": "yiddish",
    "Japanese": "japanese",
    "Tolkien": "tolkien",
    "Rock Groups": "rock-groups",
    "Music: Classical": "music-classical",
    "Music: Country": "music-country",
    "Music: Jazz": "music-jazz",
    "Movie Characters": "movie-characters",
}

selected_word_list = "English"


class FontNameGenerator:
    def __init__(
        self,
        word_lists=word_lists,
        word_list=None,
        min_length=min_length,
        max_length=max_length,
        ideal_length=ideal_length,
        length_influence=length_influence,
        first_letters=first_letters,
        other_letters=other_letters,
        prefix=name_prefix,
        suffix=name_suffix,
        cutoff_score=cutoff_score,
    ):
        self.find_word_list_dir()

        self.word_lists = word_lists
        self.word_list = word_list  # Name
        self.min_length = min_length
        self.max_length = max_length
        self.ideal_length = ideal_length
        self.length_influence = length_influence
        self.first_letters = first_letters
        self.other_letters = other_letters
        self.prefix = prefix
        self.suffix = suffix
        self.cutoff_score = cutoff_score

    def find_word_list_dir(self):
        self.base_path = Path(__file__).parent
        for _ in range(3):
            self.word_list_dir = self.base_path / "wordlists"
            if self.word_list_dir.exists():
                break

            self.base_path = self.base_path.parent
        # print(f"Base path: {self.base_path}")
        # print(f"Word lists in {self.word_list_dir}")

    @property
    def word_list(self):
        return self._word_list

    @word_list.setter
    def word_list(self, value):
        if value is None:
            self._word_list = None
            return

        # Set word list by name
        if value in self.word_lists:
            self.word_list_filename = self.word_lists[value]
            self.load_wordlist()
            self._word_list = value
        else:
            self._word_list = None
            print("Unknown word list: %s" % value)

    @property
    def selected_word_list(self):
        return self.word_list_filename

    @selected_word_list.setter
    def selected_word_list(self, value):
        self._selected_word_list = value
        self.word_list_filename = self.word_lists[
            sorted(self.word_lists.keys())[self._selected_word_list]
        ]
        self.load_wordlist()

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
                    f.write(
                        "%s%s%s%s\n" % (self.prefix, w[0].upper(), w[1:], self.suffix)
                    )
            else:
                break
        f.close()

    def write_csv(self, the_dict) -> None:
        f = codecs.open("found_names.csv", "wb", "utf-8")
        f.write('"Name";"Score";"Letter Uniqueness";"Length Score"\n')
        for s in sorted(the_dict.keys(), reverse=True):
            if s > 0.5:
                for w, r, d in sorted(the_dict[s]):
                    f.write(
                        '"%s%s%s";"%s";"%s";"%s"\n'
                        % (
                            self.prefix,
                            w.title(),
                            self.suffix,
                            int(round(s, 1) * 10),
                            int(round(r, 1) * 10),
                            int(round(d, 1) * 10),
                        )
                    )
            else:
                break
        f.close()

    def load_wordlist(self) -> None:
        file_path = (self.word_list_dir / self.word_list_filename).with_suffix(".txt")
        with codecs.open(str(file_path), "rb", "utf-8") as txt_file:
            self.words = [line.strip() for line in txt_file]

    def get_diff_score(self, word) -> float:
        deviation_score = 1.0
        diff = len(word) - int(self.ideal_length)
        if diff < 0:
            deviation_score = 1 - self.length_influence * float(abs(diff)) / (
                int(self.ideal_length) - int(self.min_length)
            )
        elif diff > 0:
            deviation_score = 1 - self.length_influence * float(abs(diff)) / (
                int(self.max_length) - int(self.ideal_length)
            )
        return deviation_score

    def get_filtered_words(self):
        filtered_words = {}

        for w in self.words:
            if int(self.min_length) <= len(w) <= int(self.max_length):
                score = 0.0
                for letter in w[1:]:
                    if letter in self.other_letters:
                        score += 1
                repetition = (1 + len(set(list(w))) / float(len(w))) / 2
                score = score / len(w)
                score = repetition * score
                deviation = self.get_diff_score(w)
                score = deviation * score
                if w[0].upper() in self.first_letters:
                    score *= 2
                score = round(score, 2)
                if score in filtered_words:
                    filtered_words[score].append((w, repetition, deviation))
                else:
                    filtered_words[score] = [(w, repetition, deviation)]
        final_words = {
            score: words
            for score, words in filtered_words.items()
            if score > self.cutoff_score
        }
        return self.prefix, self.suffix, final_words


if __name__ == "__main__":
    fng = FontNameGenerator(
        word_lists,
        selected_word_list,
        min_length,
        max_length,
        ideal_length,
        length_influence,
        first_letters,
        other_letters,
        name_prefix,
        name_suffix,
        cutoff_score,
    )
    print(fng.get_filtered_words())
    # draw_words(filtered_words)
    # Write results to file
    # write_csv(filtered_words)
    # write_txt(filtered_words)
