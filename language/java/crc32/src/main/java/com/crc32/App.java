import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.zip.CRC32;
import java.util.zip.CheckedInputStream;

/**
 * Hello world!
 *
 */
public class App 
{
    private static void doChecksum(String fileName) {
        try {
            CheckedInputStream cis = null;
            long fileSize = 0;
            try {
                // Computer CRC32 checksum
                cis = new CheckedInputStream(new FileInputStream(fileName), new CRC32());
                fileSize = new File(fileName).length();
            } catch (FileNotFoundException e) {
                System.err.println("File not found.");
                System.exit(1);
            }
            byte[] buf = new byte[128];
            while(cis.read(buf) >= 0) {
            }
            long checksum = cis.getChecksum().getValue();
            System.out.println(checksum + " " + fileSize + " " + fileName);
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    public static long getByteCrc32(byte[] data){
        CRC32 crc32 = new CRC32();
        crc32.update(data);
        return crc32.getValue();
    }

    /**
     * Sole entry point to the class and application.
     * @param args Array of String arguments.
     * @throws IOException 
     * @throws FileNotFoundException 
     */
    public static void main(String[] args) throws FileNotFoundException, IOException {
        String   merge = "xxxxxxgegjelgjelgjelgxx";
        long     value = getByteCrc32(merge.getBytes());

        
    }
}
