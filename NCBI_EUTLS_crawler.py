import urllib.request as ULR
import LightLinter as LL
import time as TI
##import pickle as PI
import codecs


DI = {'base':'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
      'inxx_file':'InxxFile.xml',
      'ArtinxxLI':[],
      'ainx':0,     ## article index
      'outfinx':0      ## outfile index
      }


def Fetch():

    print('Fetch: start ===== >>>> ')
    
    ainx = DI['ainx']

    ArtInxxLI = DI['ArtinxxLI'][ainx:ainx+10]
    
    
    inxx_fr = ','.join(ArtInxxLI)

    base = DI['base']

    fetch_declaration = 'efetch.fcgi?db=pubmed&id='
    rettype = "&rettype=abstract&retmode=json"

#    fetch__ul = base + "efetch.fcgi?db=pubmed&id=26051947,26032638"+rettype

    FetchLI = [base,
               fetch_declaration,
               inxx_fr,
               rettype
               ]

    fetch__ul = ''.join(FetchLI)
    print('fetch__ul', fetch__ul)
        
    result = ULR.urlopen(fetch__ul)
    bymol = result.read()
#    print('\n\n', bymol, '\n\n')
   # text = line.decode('utf-8')

    bysl = bymol.split(b'\n\n\n')

    out_dna = LL.TKDI['en']['out_dir'].get()
    outfile_prefix = LL.TKDI['en']['outfile'].get()
    
    for y in range(len(bysl)):

        by_outline = bysl[y]

        outfinx = DI['outfinx']
        outfile = out_dna +'/' + outfile_prefix +'_'+str(outfinx)+'.txt'
        DI['outfinx'] += 1
        
        #try:
            #outline = by_outline.decode('utf-8')
        outline = codecs.decode(by_outline)
        fi = open(outfile, 'w')
        outline = str(by_outline)
        line = outline.replace('\\n', '\n')
        #PI.dump(outline, fi)
        fi.write(line)
        fi.close()
        #except:
        #    print(outfinx, 'not written')

#    counter += 1
    
    DI['ainx'] += 10
    
    print('Fetch: local job is done')



def TimeFetcher():

   # total = 580
    lin_total = LL.TKDI['en']['retmax'].get()
    total = int(lin_total)

    limit = total/10
    limit = int(limit)
    
    print('limit:', limit)
    
                          
    for y in range(limit):

        TI.sleep(2)

        LocTime = TI.localtime()

        curr_min = LocTime.tm_min
        curr_sec = LocTime.tm_sec

        print(curr_min, curr_sec)


        Fetch()
        


def Fetch__10():

    ArtInxxLI = DI['ArtinxxLI'][:10]
    inxx_fr = ','.join(ArtInxxLI)

    base = DI['base']

    fetch_declaration = 'efetch.fcgi?db=pubmed&id='
    rettype = "&rettype=abstract&retmode=text"

#    fetch__ul = base + "efetch.fcgi?db=pubmed&id=26051947,26032638"+rettype

    FetchLI = [base,
               fetch_declaration,
               inxx_fr,
               rettype
               ]

    fetch__ul = ''.join(FetchLI)
    print('fetch__ul', fetch__ul)
        
    result = ULR.urlopen(fetch__ul)
    bymol = result.read()
    print('\n\n', bymol, '\n\n')
   # text = line.decode('utf-8')

    bysl = bymol.split(b'\n\n\n')

    out_dna = LL.TKDI['en']['out_dir'].get()

    outfile_prefix = LL.TKDI['en']['outfile'].get()
    
    for y in range(len(bysl)):

        by_outline = bysl[y]
        
        outfile = out_dna  +'/' + outfile_prefix +'_'+str(y)+'.txt'
        
        try:
            outline = by_outline.decode('utf-8')            
            fi = open(outfile, 'w')
            fi.write(outline)
            fi.close()
        except:
            print(y, 'not written')


    print('Get__abstracts: done')
    

    
def Read__inxx__file():

    inxx__file = DI['inxx_file']
    
    fi = open(inxx__file, 'r')
    ls = fi.read()
    fi.close()

    count_start = ls.find('<Count>')
    count_start_pos = count_start + 7
    count_end = ls.find('</Count>')

    art_count = ls[count_start_pos:count_end]
    LL.TKDI['en']['art__count'].put(art_count)

                      

    print(type(ls))
    ls = ls.replace('<Id>', '')
    ls = ls.replace('</Id>', '::')

    sl = ls.split('::')

    inxx_array = []

    for si in sl:
        si = si.strip()
        if si.isdigit() == True:
            inxx_array.append(si)

    DI['ArtinxxLI'] = inxx_array
    
    LL.Fill__lx(inxx_array, 'artinxx')   


    

def Get__inxx():
    
    db = 'pubmed'
#    query = 'bisoprolol'
    query = LL.TKDI['en']['query'].get()
    query = query.replace(' ', '+')

    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    search_declaration = 'esearch.fcgi?db=pubmed&term='

    retstart = LL.TKDI['en']['retstart'].get()
    retmax   = LL.TKDI['en']['retmax'].get()
    
    sl_rr = ['&retstart=',
             retstart,
             '&retmax=',
             retmax] 
    ret_range = ''.join(sl_rr)
    
##    the_primer = base + "esearch.fcgi?db="+\
##                 db+"&term="+query #+"&retstart=97&retmax=50" #+'&usehistory=y"
##    print(the_primer)
    
    SearchLI = [base,
               search_declaration,
               query,
               ret_range
               ]

    the_primer = ''.join(SearchLI)
    
    file_name = DI['inxx_file'] #'bisopr_inxx.xml'
    result = ULR.urlopen(the_primer)
    raw_line = result.read()
    print('type(raw_line):', type(raw_line))

    text = raw_line.decode('utf-8')    
    print('type(text):', type(text))
    
    sl = text.split('</')    
    LL.Fill__lx(sl, 'artinxx')   
##
    
    fi = open(file_name, 'w')
    fi.write(text)
    fi.close()

    print('Get__inxx: done')


def Get__abstracts():

    base = DI['base']

    rettype = "&rettype=abstract&retmode=text"

    fetch__ul = base + "efetch.fcgi?db=pubmed&id=26051947,26032638"+rettype
    result = ULR.urlopen(fetch__ul)
    text = result.read().decode('utf-8')

    fi = open('first_bisoprolol_abstracts.txt', 'w')
    fi.write(str(text))
    fi.close()


    print('Get__abstracts: done')


    

def Create__menu():

    LL.Create__menu()

    LL.TKDI['me'][1] = LL.TK.Menu(LL.TKDI['me'][0])    
    LL.TKDI['me'][1].add_command(label = 'Get article indexes', command = Get__inxx)
    LL.TKDI['me'][1].add_command(label = 'Read index file',   command = Read__inxx__file)

    LL.TKDI['me'][2] = LL.TK.Menu(LL.TKDI['me'][0])
##    LL.TKDI['me'][2].add_command(label = 'Fetch__10',   command = Fetch__10)
    LL.TKDI['me'][2].add_command(label = 'Crawler: GET ABSTRACTS FROM NCBI',   command = TimeFetcher)
##    LL.TKDI['me'][2].add_command(label = 'Refsi_with',   command = Refsi_with)
##    
##

    LL.TKDI['me'][0].add_cascade(label = 'Create Set',   menu = LL.TKDI['me'][1])
    LL.TKDI['me'][0].add_cascade(label = 'FETCH',      menu = LL.TKDI['me'][2])
##    LL.TKDI['me'][0].add_cascade(label = 'Primers', menu = LL.TKDI['me'][3])
##    LL.TKDI['me'][0].add_cascade(label = 'Search',  menu = LL.TKDI['me'][4])

def Create__forms():

    LL.Create__root('Amorpha EUTL Crawler')

    LL.Add__one__frame(0, 'root', 1, 1)

    LL.Add__one__frame(1, 0, 1, 1)
    LL.Add__entry('art__count', 1, 1, 1, 10, 'Arial 14')
    LL.Add__entry('retstart',   1, 2, 1, 10, 'Arial 14')
    LL.Add__entry('retmax',     1, 3, 1, 10, 'Arial 14')
    LL.Add__entry('query' ,     1, 4, 1, 20, 'Arial 14')
    LL.Add__entry('outfile' ,   1, 5, 1, 20, 'Arial 14')
    LL.Add__entry('out_dir' ,   1, 7, 1, 25, 'Arial 11')

    LL.TKDI['en']['retstart'].put(0)
    LL.TKDI['en']['retmax'].put(20)
    LL.TKDI['en']['query'].put('aspirin[Title]')
    LL.TKDI['en']['outfile'].put('aspirin')
    LL.TKDI['en']['out_dir'].put('Aspirin_abstracts')
    
    LL.Add__one__frame(2, 0, 2, 1)
    LL.Add__lx('artinxx', 2, 1, 1, 15, 10, 'Arial 16')

    Create__menu()
    
  

def Start():


    Create__forms()
#    Get__inxx()
#    Read__inxx__file()

Start()

LL.TKDI['fr']['root'].mainloop()
    


