#include <cs50.h>
#include <stdio.h>

int get_start_size();
int get_end_size(int startsize);
int get_years(int startsize, int endsize);
void print_numbers(int startsize, int endsize, int years);

int main(void)
{
    // TODO: Prompt for start size
    int startsize = get_start_size();

    // TODO: Prompt for end size
    int endsize = get_end_size(startsize);

    // TODO: Calculate number of years until we reach threshold
    int years = get_years(startsize, endsize);

    // TODO: Print number of years
    print_numbers(startsize, endsize, years);
}

int get_start_size()
{
    int n;
    do
    {
        n = get_int("Startpopulation: ");
    }
    while (n < 9);
    return n;
}

int get_end_size(int startsize)
{
    int e;
    do
    {
        e = get_int("Endpopulation: ");
    }
    while (e < startsize);
    return e;
}

int get_years(int startsize, int endsize)
{
    int population = startsize;
    int years = 0;
    while (population < endsize)
    {
        population += (population / 3) + -(population / 4);
        years++;
    }
    return years;
}

void print_numbers(int startsize, int endsize, int years)
{
    printf("Start size: %i\nEnd size: %i\nYears: %i", startsize, endsize, years);
}