#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get string from user
    string s = get_string("Text: ");

    // Count number of letters, words and sentences
    int letters = count_letters(s);
    int words = count_words(s);
    int sentences = count_sentences(s);

    printf("%i %i %i\n", letters, words, sentences);

    // Calculate Grade
    double L = (double) letters / (double) words * 100;
    double S = (double) sentences / (double) words * 100;
    double index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    // Output Grade
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (islower(text[i]) || isupper(text[i]))
        {
            letters += 1;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 0;
    bool singleSpace = true;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ' && singleSpace)
        {
            singleSpace = false;
            words += 1;
        }
        else if (text[i] != ' ')
        {
            singleSpace = true;
        }
    }
    if (strlen(text) != 0)
    {
        return words + 1;
    }
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;
    bool singleSpace;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences += 1;
        }
    }
    return sentences;
}
