def transcriber(text):

#Resources
    import resources as res

#Indexes and variables
    text = list(text)
    output = []
    i_t = 0
    i_o = 0

#Whitespace to add a final index (workaround)
    text.append("")


#Function starts
    while i_t < len(text):

#Rules for unvariable consonants:
        if text[i_t] in res.map_unvar:
            output.append(res.map_unvar[text[i_t]])
            i_t += 1
            i_o += 1

#---------------------------------------------------------------
#Rules for "c"
        elif text[i_t] == "c":

#Rule for "ch"
                if text[(i_t)+1] == "h":
                    output.append("tS")
                    i_t += 2
                    i_o += 1

#Rule for ce, ci
                elif text[(i_t)+1] == "e" or text[(i_t)+1] == "i":
                    output.append("s")
                    i_t += 1
                    i_o += 1
        
#Rule for "c" = /k/
                elif text[(i_t)] == "c":
                    output.append("k")
                    i_t += 1
                    i_o += 1


#---------------------------------------------------------------
#Rules for "q"

        elif text[i_t] == "q":
            
#Rule for "qu"
            if text[(i_t)+1] == "u":
                output.append("k")
                i_t += 2
                i_o += 1

#Rule for other "q"'s
            else:
                output.append("k")
                i_t += 1
                i_o += 1

#Rule for "sh"
        elif text[i_t] == "s":
            if text[(i_t)+1] == "h":
                output.append("S")
                i_t += 2
                i_o += 1

#Rule for other "s"
            else:
                output.append("s")
                i_t += 1
                i_o += 1
      
#Rules for initial r = "r"
        elif text[i_t] == "r" and i_t == 0:
            output.append("r")
            i_t += 1
            i_o += 1

        elif text[i_t] == "r" and text[(i_t)-1] == " ":
            output.append("r")
            i_t += 1
            i_o += 1

        elif text[i_t] == "r" and text[(i_t)-1] in res.cons_r:
            output.append("r")
            i_t += 1
            i_o += 1

#Rule for "r = 4"
        elif text[i_t] == "r":
            if text[(i_t)+1] != "r":
                output.append("4")
                i_t += 1
                i_o += 1

#Rule for "rr = r"            
            elif text[(i_t)+1] == "r":
                output.append("r")
                i_t += 2
                i_o += 1

#Rules for "l"
#Rule for "ll"
        elif text[i_t] == "l":
            if text[(i_t)+1] == "l":
                output.append("j")
                i_t += 2
                i_o += 1

#Rule for "l"
            else:
                output.append("l")
                i_t += 1
                i_o += 1

#Rule for "h"
        elif text[i_t] == "h":
                i_t += 1
                i_o += 1


#Rules for allophony of "b"
#Rule for absolute onset
        elif text[i_t] == "b" and i_t == 0:
            output.append("b")
            i_t += 1
            i_o += 1

#Rules for intervocalic "b"
#Word-boundary intervocalic
        elif text[i_t] == "b" and (text[(i_t)-1] == " " and text[(i_t)-2] in res.vowels):
            output.append("B")
            i_t += 1
            i_o += 1

#Same-word intervocalic
        elif text[i_t] == "b":
            if text[(i_t)+1] in res.vowels and text[(i_t)-1] in res.vowels:
                output.append("B")
                i_t += 1
                i_o += 1
        
#After consonants (not "m")
        elif text[i_t] == "b":
            if text[(i_t)-1] in res.cons_B:
                output.append("B")
                i_t += 1
                i_o += 1    

#After "m"
        elif text[i_t] == "b":
            if text[(i_t)-1] == "m":
                output.append("b")
                i_t += 1
                i_o += 1    

#FALLBACK


        else:
            output.append(text[i_t])
            i_t += 1
            i_o += 1
            
    print(sys.argv)
    print(output)
    return output
    



#Rules for b/B

#Rules for g/G

#Rules for gu

#Rules for d/D

#Rules for i/j

#Rules for u/w

#Rules for graphic stress

#Rules for implicit stress
