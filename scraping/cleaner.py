#cleaning input from https://randomwordgenerator.com/would-you-rather-question.php
def main():
    lineDict = {}
    f = open('output.txt')
    output = open('output_cleaned.txt', 'w')
    for line in f:
        if line not in lineDict and line[-2] == '?':
            output.write(line + '\n')
            lineDict[line] = 1 

if __name__ == '__main__':
    main()