"""Подсчёт гласных, согласных и каждой из пяти гласных."""


def count_letters(word):
    vowels = {letter: word.count(letter) for letter in "aeiou"}
    vowel_count = sum(vowels.values())
    return vowel_count, len(word) - vowel_count, vowels


def main():
    word = input().strip()
    vowels, consonants, counts = count_letters(word)
    print("Гласных:", vowels)
    print("Согласных:", consonants)
    for letter, count in counts.items():
        print(f"{letter}:", count if count else False)


if __name__ == "__main__":
    main()
