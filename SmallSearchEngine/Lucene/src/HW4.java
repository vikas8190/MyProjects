import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.Pattern;
import java.io.FileWriter;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.util.Bits;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.search.DocIdSetIterator;
import org.apache.lucene.index.DocsEnum;
import java.util.HashMap;
import java.util.Map;
import java.nio.file.*;
import java.nio.charset.Charset;
import java.util.regex.Matcher;
/**
 * To create Apache Lucene index in a folder and add files into this index from the folder CACM
 */
public class HW4 {
    private static Analyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
    String s="Indexer";
    // Create the index folder if it doesnt exists
    File IndexFolder=new File(s);
    if(!IndexFolder.exists())
    {
    	IndexFolder.mkdirs();
    } 
    // Delete all the files present in the Index Folder
	for(File file: IndexFolder.listFiles())
	{
		file.delete();
	}
	// Delete existing Results file where the Top Rank results are pushed in
	File ResultsFile=new File("Results.txt");
    if (ResultsFile.exists())
    	ResultsFile.delete();
	HW4 indexer = null;
	try {
	    indexer = new HW4(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}
	// For each file in CACM call the indexing function
	File cacm_folder =new File("CACM/");
	File[] listofcacm_files=cacm_folder.listFiles();
	
	for(File cacm_file: listofcacm_files){
		try {
			s="CACM/"+cacm_file.getName();
			// Remove all the unwanted tags from the input file to be indexed
			indexer.RemoveTags(s);
			// Call the function to index the file from which tags has been removed
			indexer.indexFileOrDirectory(s);
		}
		catch (Exception e) {
			System.out.println("Error indexing " + s + " : "
				+ e.getMessage());
		    }	
	}
	System.out.println("***********************************************");
	System.out.println("Indexing completed");
	System.out.println("***********************************************");
	
	
	
	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	File queryfile=new File("queryfile.txt");
	Scanner sr = new Scanner(queryfile);
	String s1;
	// Get the top ranked query for each of the query in the queryfile.txt
	while (sr.hasNextLine()){
	    try {
	    	s1=sr.nextLine();

	    	indexer.GetTopRanked(s1);
	    	}
	    catch (Exception e) {
	    	System.out.println("Error searching " + s + " : "
			+ e);
	    	}
	    }
	sr.close();
	System.out.println("Gathered Top Ranking document info for queries into Results.txt");
	System.out.println("***********************************************");
	
	indexer.GetFrequencyDetails();
	System.out.println("Gathered word-frequency details into IndexStats.txt");
	System.out.println("***********************************************");
	}


    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    HW4(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
		analyzer);

	writer = new IndexWriter(dir, config);
    }

    /* Remove all the tags which are present in the filename given as input*/
    public void RemoveTags(String s) throws IOException
    {
    	Path index_file_path=Paths.get(s);
    	Charset charset=StandardCharsets.UTF_8;
    	String file_content=new String(Files.readAllBytes(index_file_path),charset);
    	file_content=file_content.replaceAll("<.*>","");
    	Files.write(index_file_path,file_content.getBytes(charset));
    }
    
    /*Read the index file created and get term by term and update its frequency to a hashmap
     * The details are pushed into file IndexStats.txt*/
    public void GetFrequencyDetails() throws IOException 
    {
    	String indexLocation="Indexer";
    	IndexReader indexReader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
    	Bits liveDocs = MultiFields.getLiveDocs(indexReader);
        HashMap<String,Integer> doc_stats= new HashMap<String,Integer>();
        String word;
        Integer doc_count;
        TermsEnum termEnum = MultiFields.getTerms(indexReader, "contents").iterator(null);
        BytesRef bytesRef;
       while ((bytesRef = termEnum.next()) != null) 
       {
    	   if (termEnum.seekExact(bytesRef))
           {
    		   DocsEnum docsEnum = termEnum.docs(liveDocs, null);
               if (docsEnum != null) 
               {
            	   while (docsEnum.nextDoc() != DocIdSetIterator.NO_MORE_DOCS) 
                   {
            		   word=bytesRef.utf8ToString();
                       if(doc_stats.containsKey(word))
                       {
                    	   doc_count=doc_stats.get(word);
                    	   doc_stats.put(word,doc_count+docsEnum.freq());
                       }
                       else
                       {
                        	doc_stats.put(word,docsEnum.freq());
                       }
                    }
                }
           }
        } 
        File IndexStatsFile=new File("IndexStats.txt");
        // Delete the old IndexStats file.
        if (IndexStatsFile.exists())
        	IndexStatsFile.delete();
        FileWriter f =new FileWriter("IndexStats.txt",true);
        for(Map.Entry<String, Integer> entry : doc_stats.entrySet())
        {
            f.write(entry.getKey()+":"+entry.getValue()+"\n");
        }
        f.close();
    }
    
    /* Get the top ranked queries for the given query along with the hits for the query. For each hit
     * Also get the most relevant doc snippet that highlights the fit. This is calculated as
     * atmost 200 character words starting from the first matching word in query inside the document.
     * 
     * */
    public void GetTopRanked(String query) throws IOException 
    {
    	String indexLocation="Indexer";
    	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
    	IndexSearcher searcher = new IndexSearcher(reader);
    	TopScoreDocCollector collector = TopScoreDocCollector.create(3204, true);
        FileWriter f =new FileWriter("Results.txt",true);
    	String s = "";
    	try
    	{
    		QueryParser qp=new QueryParser(Version.LUCENE_47, "contents",analyzer);
    		Query q = qp.parse(query);
    		searcher.search(q, collector);
    		ScoreDoc[] hits = collector.topDocs().scoreDocs;
    		f.write("Found " + hits.length + " hits. for "+query+"\n");
    		f.write("*************************************************************************************"+"\n");
    		for (int i = 0; i < hits.length; ++i) 
    		{
    			int docId = hits[i].doc;
    			Document d = searcher.doc(docId);
    			f.write((i + 1) + ". " + d.get("filename")
    				    + " score=" + hits[i].score+"\n");
    			String doc_name=d.get("path");
    			String snippet;
    			snippet=GetDocSnippet(doc_name,query);
    			f.write("#####################################################"+"\n");
    		    f.write("DOCUMENT HIGHLIGHT:"+"\n");
    		    f.write(snippet+"\n");
    		    f.write("#####################################################"+"\n");
    		}
    	}
    	catch (Exception e)
    	{
    		System.out.println("Error searching " + s + " : "
    		    			 + e);
    	}
    	f.write("*************************************************************************************"+"\n");
    	f.close();
    }
    	/* Find out most relevant doc snippet. Splits word in query. For each query word , finds
    	 * out the relevant part starting from that word occcurence. the 200 characters starting
    	 * from the largest string among those matches is taken as the relevant doc snippet for the
    	 * query*/ 
    public String GetDocSnippet(String DocName,String query) throws IOException {
    	byte[] encoded=Files.readAllBytes(Paths.get(DocName));
    	String content= new String(encoded, StandardCharsets.UTF_8);
    	String[] querywords=query.split(" ");
    	int matchlength=0;
    	String snippet="";
    	for (String s: querywords)
    	{
    		Pattern p=Pattern.compile("(?i)"+s+" (?s).*[\n\r].*");
    		Matcher m=p.matcher(content);
    		String matchstring;
    		if(m.find())
    		{
    			matchstring=m.group(0);
    			if (matchstring.length()>matchlength)
    			{
    				int index=200;
    				matchstring.toString();
    				if(matchstring.length()<index)
    				{
    					index=matchstring.length();
    				}
    				snippet=matchstring.substring(0,index);
    				matchlength=matchstring.length();
    			}
    		}
    	}
    	return snippet;
    }
    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	addFiles(new File(fileName));
	for (File f : queue) 
	{
	    FileReader fr = null;
	    try 
	    {
	    	Document doc = new Document();

	    	// ===================================================
	    	// add contents of file
	    	// ===================================================
	    	fr = new FileReader(f);
	    	doc.add(new TextField("contents", fr));
	    	doc.add(new StringField("path", f.getPath(), Field.Store.YES));
	    	doc.add(new StringField("filename", f.getName(),
			Field.Store.YES));

	    	writer.addDocument(doc);
	    } 
	    catch (Exception e) 
	    {
	    	System.out.println("Could not add: " + f);
	    } 
	    finally
	    {
	    	fr.close();
	    }
	}
	queue.clear();
    }
    /* Add files to the list of files to be indexed*/
    private void addFiles(File file)
    {
    	if (!file.exists()) 
    	{
    		System.out.println(file + " does not exist.");
    	}
    	if (file.isDirectory())
    	{
    		for (File f : file.listFiles())
    		{
    			addFiles(f);
    		}
    	}
    	else 
    	{
    		String filename = file.getName().toLowerCase();
    		// ===================================================
    		// Only index text files
    		// ===================================================
    		if (filename.endsWith(".htm") || filename.endsWith(".html")
    				|| filename.endsWith(".xml") || filename.endsWith(".txt"))
    		{
    			queue.add(file);
    		}
    		else 
    		{
    			System.out.println("Skipped " + filename);
    		}
    	}
    }

    /**
     * Close the index.
     * 
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException 
    {
    	writer.close();
    }
}
