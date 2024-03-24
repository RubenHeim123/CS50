#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    // Check command-line arguments
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Input is not a WAV file.\n");
        return 1;
    }

    // Read header
    // TODO #3
    // Read infile's BITMAPFILEHEADER
    WAVHEADER wh;
    fread(&wh, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    // TODO #4
    if (check_format(wh) == 0)
    {
        printf("Invalid WAV Format\n");
        return 1;
    }

    // Open output file for writing
    // TODO #5
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open output file.\n");
        return 1;
    }

    // Write header to file
    // TODO #6
    fwrite(&wh, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    // TODO #7
    int block_size = get_block_size(wh);

    // Write reversed audio to file
    // TODO #8
    // Declare an array to store each block we read in
    BYTE buffer[block_size];

    // Move Pointer to the End (takes in the pointer, the offset amount of 0, and moves it the end of the file)
    fseek(input, 0, SEEK_END);

    // Finding the Buffer Audio Size (excluding the header)
    long audio_size = ftell(input) - sizeof(WAVHEADER);
    int audio_block = (int) audio_size / block_size;

    // Iterate through the input file audio data
    // Maintain the order of the channels for each audio block (Reversed)
    for (int i = audio_block - 1; i >= 0; i--)
    {
        // Starting From End of the File (Block by Block Transferring)
        fseek(input, sizeof(WAVHEADER) + i * block_size, SEEK_SET);
        fread(buffer, block_size, 1, input);
        fwrite(buffer, block_size, 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{
    // TODO #4
    BYTE check[] = {'W', 'A', 'V', 'E'};
    for (int i = 0; i < 4; i++)
    {
        if (header.format[i] != check[i])
        {
            return 0;
        }
    }
    return 1;
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    WORD bytePerSample = header.bitsPerSample / 8;
    return (header.numChannels * bytePerSample);
}