import re;

def consoleToResults(inputpath, outputpath):
    """Takes the raw output of an SOS program (inputpath) run and
       extracts the max/avg starve times for each process to (outputpath)"""

    #python overwrites duplicate-key entries in dictionaries, so each
    #post-parse dictionary value is guaranteed to be the final appearance
    #of its respective key in the output file
    
    #output is a dictionary that stores ProcessId:max,avg,,max,avg...etc
    #each output is stored in a dictionary entry where the key is the line
    #of output containing the process id.
    output = dict();

    with open(inputpath) as f:
        content = f.readlines()

    #loop over each line in content
    for i in range(0, len(content)):
        match = re.search("Process id [0-9]+", content[i])
        if match == None:
            continue;

        else:
            output[match.group(0)] = content[i+1];


    #write to file
    outputf = open(outputpath, 'w');
    for k in output.keys():
        outputf.write(k + ":\n")
        outputf.write("\t" + output[k] + "\n")

    outputf.close();

def resultsToCsv(inputpaths, outputpath):
    """Takes a list of file paths (inputpaths) containing results created by
       #consoleToResults, creates a comma-separated list, and writes it to (outputpath)"""

    #dictionary stores the row for each
    output = dict()
    lines = []

    with open(inputpaths[0]) as f:
        content = f.readlines()


    #loop over files
    for i in range(0, len(inputpaths)):
        with open(inputpaths[i]) as f:
            content = f.readlines()

        #loop over lines in files[i]
        for j in range(0, len(content)):
            match = re.search("Process id [0-9]+", content[j])
            if match == None:
                continue

            else:
                nextLine = content[j + 1];
                maxStarve = findMaxStarve(nextLine)
                avgStarve = findAvgStarve(nextLine)
                key = match.group(0)[11:]

                #conditionally initialize or append if key doesn't exist
                if key not in output:
                    output[key] = maxStarve + "," + avgStarve + ",,"

                else:
                    output[key] += maxStarve + "," + avgStarve + ",,"


    outputf = open(outputpath, "w")

    #write to file
    for k in output.keys():
        lines.append(k + "," +output[k] + "\n")

    outputf.writelines(lines)
        


def findMaxStarve(str):
    """Matches the max starve time in a string and returns it
       NOTE: has some sketchy behavior if the console output
       follows the process id with something like --------------
       such as in the case of the idle process"""

    pattern = "Max Starve Time: \-?[0-9]+(\.[0-9]+)?"
    match = re.search(pattern, str)
    if match == None:
        return None

    match = match.group(0)
    match = match[17:]

    return match


def findAvgStarve(str):
    """Matches the max starve time in a string and returns it
       NOTE: has some sketchy behavior if the console output
       follows the process id with something like --------------
       such as in the case of the idle process"""

    pattern = "Avg Starve Time: \-?[0-9]+(\.[0-9]+)?"
    match = re.search(pattern, str)
    if match == None:
        return None

    match = match.group(0);
    match = match[17:]

    return match
