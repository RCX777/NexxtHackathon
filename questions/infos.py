def get_data(business, output_file="data.txt"):
    # Ask the chat for the information about the business
    que = f"""Please provide me the following information about {business}: Key Facts, Services and Features, 
        Notable Innovations and Initiatives, Subsidiaries and Partnerships, Reputation and Trustworthiness and Challenges."""
    
    ans = ""

    with open(output_file, 'w'):
        output_file.write(ans)

def ask_question(q):
    ans = ""
    # Ask chat the quesion
    if ans == "yes":
        return 1 
    else:
        return 0

if __name__ == '__main__':
    trustworthyness = 0

    file1 = "data.txt"
    file2 = "questions.txt"

    with open(file1, 'r', encoding='utf-8') as f1:
        lines1 = f1.readlines()

    with open(file2, 'r', encoding='utf-8') as f2:
        lines2 = f2.readlines()

    l = "With these information, please ask with true or false to the following question:\n"
    for line2 in lines2:
        concatenated_line = "".join(lines1) + "\n" + l + line2
        print(concatenated_line)
        # trusttworthyness += ask_question(concatenated_line)

    if trustworthyness >= 60:
        print("The site is trustworthy")
    else:
        print("The site can be malicious ")


