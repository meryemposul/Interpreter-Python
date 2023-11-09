import sys


def parse_commands(lines):
    commands_list = []
    current_list = []

    for line in lines:
       # line = line.strip()

        if '=' in line  and  not line.startswith('    '):
            if current_list and line.startswith('    ') or '=' not in line :
                commands_list.append(current_list.copy())
            current_list= [line, None]
            #commands_list.append(current_block.copy())

            #current_block=[line]

        elif line.startswith('eger ') or line.startswith('mery ') or line.startswith('degılse'):
           #current_block[0] = line
           if current_list:

               commands_list.append(current_list.copy())
               current_list= []
               current_list = [line]


        elif line.startswith('    '):

            current_list.append(line[4:])
            if  '='  in line:
               # current_block.append(line[4:])
               commands_list.append(current_list.copy())
               #current_list = []


        else:
            if current_list:
                commands_list.append(current_list.copy())
           # commands_list.append(line)
            current_list = []

    return commands_list



def evaluate_commands(lines):
    parsed_commands = parse_commands(lines)
    print(parsed_commands)

def help():
    print("Bu kod işlem ifadesi, yaz ve eger içermektedir.")

def main():
    if len(sys.argv) < 2:
        file_name = "abc.ty"
        with open(file_name, 'r') as file:
            lines = file.readlines()
        evaluate_commands(lines)
    else:
        file_name = sys.argv[1]
        if file_name == "-h":
            help()
        else:
            try:
                with open(file_name, 'r') as file:
                    lines = file.readlines()
                evaluate_commands(lines)
            except FileNotFoundError:
                print(f"{file_name} adlı dosya bulunamadı")

if __name__ == "__main__":
    main()

