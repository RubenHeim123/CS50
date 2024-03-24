#include <cs50.h>
#include <stdio.h>

int get_height();
void print_pyramid(int height);
void print_hashes(int num);

int main(void)
{
    // get height
    int height = get_height();

    // prompt
    print_pyramid(height);
}

int get_height()
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (1 > n || n > 8);
    return n;
}

void print_pyramid(int height)
{
    for (int j = 1; j <= height; j++)
    {
        // print hashes(height)
        for (int f = 0; f < height - j; f++)
        {
            printf(" ");
        }
        print_hashes(j);
        for (int i = 0; i < 2; i++)
        {
            printf(" ");
        }
        print_hashes(j);
        printf("\n");
    }
}

void print_hashes(int num)
{
    for (int e = 0; e < num; e++)
    {
        printf("#");
    }
}