#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool check_key(string s);
string get_cipher(string s, string key);

int main(int argc, string argv[])
{
    // Check Key
    if (argc == 2 && check_key(argv[1]))
    {
        // Get Plaintext
        string s = get_string("plaintext: ");

        // transform to ciphertext
        string cipher = get_cipher(s, argv[1]);

        // Output ciphertext
        printf("ciphertext: %s\n", cipher);
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
}

bool check_key(string s)
{
    int n = strlen(s);
    if (strlen(s) != 26)
    {
        return false;
    }

    for (int i = 0; i < n; i++)
    {
        if (!isalpha(s[i]))
        {
            return false;
        }

        for (int k = i + 1; k < n; k++)
        {
            if (s[i] == s[k])
            {
                return false;
            }
        }
    }
    return true;
}

string get_cipher(string s, string key)
{
    string cipher = s;

    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (islower(s[i]))
        {
            cipher[i] = tolower(key[s[i] - 97]);
        }
        else if (isupper(s[i]))
        {
            cipher[i] = toupper(key[s[i] - 65]);
        }
    }
    return cipher;
}
