import java.io.*;
import java.util.*;
import java.time.*;
import java.text.*;
import java.math.*;
public class Deception {
    static FastReader FastReader = new FastReader();
    static BufferedWriter o = new BufferedWriter(new OutputStreamWriter(System.out));
    static PrintWriter pw;

    static char table[] = {
            'd', 'y', 'n', 'm', 'r', '7', '2', '3', '9', '8', 'o', '2', 'm', 'n', 'y', 'l', 'r', 'f', '7', '4', '9',
            '0', '2', '3', 'q', 'y', 'n', 'd', '7', '8', '9', '4', '2', '3', 'y', 'd', '8', '9', 'o', 'q', '7',
            's', 'n', 'g', 'y', 'u', 'i', '2', 'g', 'h', 'u', 'y', 'i', 'c', 'g', 'i', 'k', 'a', 'd', 'l', 'd',
            'g', 'h', 'i', 'w', 'k', 'a', 'l', 'S', 'D', 'H', 'N', 'Q', 'O', '3', '2', '7', 'D', 'Q', '2', 'O',
            '8', 'G', 'D', 'H', '7', '8', 'O', '2', 'Q', 'D', 'N', 'G', 'W', 'U', 'A', 'K', 'D', 'G', 'H', 'X',
            'K', 'J', 'S', 'A', 'G', 'D', '2', 'K', 'S', 'A', 'G', 'I', 'K', 'G', 'I', 'Y', 'K', 'G', 'I', 'K',
            '7', 'i', 'k', 'l', 'f', 'g', '3', 'i', 'k', 'r', 'g', 'f', '3', '8', 'o', '4', '7', 't', 'g', '3',
            '9', '8', 'o', 'f', 'g', 'o', '7', 'i', 'h', 'f', 'k', 'u', 'i', 'a', 'l', 'w', 'e', 'h', 'f', 'i',
            'l', 'w', 'k', 'a', '}', 'h', 'x', 'w', 'l', 'a', 'u', 'k', 'f', 'x', 'n', 'h', 'e', 'a', 'o', 'i',
            'u', 'h', 'x', 'f', 'g', 'a', 'w', 'i', 'o', 'u', 'y', 'g', 'h', 'e', 'a', 'w', '8', 'o', 'n', '7',
            '4', 'w', 'f', '8', 'o', 'n', 'w', 'q', 'g', '7', '8', 'o', '4', 'w', 'a', 'n', 'g', 'h', 'u', 'i',
            'a', 'w', 'e', 'k', '0', 'l', 'f', 'b', 'x', 'c', 'j', 'k', 'a', 's', 'd', 'f', 'b', 'j', 'k', 'a',
            's', 'e', 'f', 'k', 'j', 'a', '7', 'e', 'n', 'f', 'g', 'a', 'i', 'u', 'y', 'w', 'e', 'k', 'f', 'g',
            'y', 'u', 'w', 'e', 'a', 'i', 'o', 'g', 'h', 'x', 'f', 'a', 'e', 'j', 'k', 'w', 'B', 'f', 'w', 'e',
            'a', 'k', 'j', 'f', 'g', 'h', 'a', 'w', '7', 'g', 'v', 'a', 'w', 'u', 'b', 't', '3', '2', 'q', '6',
            '7', '8', 'd', 't', 'b', '3', 'q', '6', '8', 'o', '4', 't', 'q', '7', '8', 'o', 'i', '3', 't', 'r',
            'o', '8', 'c', '7', 'b', 't', '3', '5', 'p', '9', 'q', 't', 'y', '5', 'c', '7', '1', 'b', 'r', 't',
            'c', 'y', '2', '7', '1', '8', 'f', '2', '7', '1', '8', '9', '0', '7', 'n', 'y', '0', '9', '8', 'y',
            'm', 'r', '8', '9', '2', 'm', 'c', '0', '9', '2', 'y', 'i', 'o', 'h', 'u', 'i', 'w', 'h', 'i', 'l',
            'w', 'n', 'h', 'r', 'i', 'u', 'w', 'e', 'k', 'l', 'h', 'n', '8', '2', '7', '0', '3', 'n', 'y', 'r',
            '7', '4', 'j', '3', 'y', 'n', 'r', '7', '8', '3', 'n', 'g', 'h', 'c', 'e', '7', 'u', 'n', 'g', 'c',
            'h', 'o', '3', '7', 'i', '4', 'y', 'h', 'r', 'o', 'i', 'u', 'w', 'e', 'h', 'r', 'i', 'o', 'w', 'n',
            'r', 'u', 'w', 'e', 'i', 'r', 'h', 'n', 'w', 'o', 'u', 'i', 'e', 'n', 'h', 'r', 'i', 'u', 'i', '3',
            'e', 'w', 'n', 'h', 'u', 'i', 'w', 'o', 'h', 'c', 'm', 'r', '7', '8', '4', 'n', 'y', '3', '7', '9',
            '8', '4', '4', '5', '4', '4', '6', 't', '4', '3', '7', '8', '9', '5', '6', '3', '9', '8', '7', 'c',
            'n', 't', '5', 'y', '9', '3', '4', '7', '8', 'n', '5', 't', 'y', 'c', '7', '8', '9', '3', '4', '6',
            'c', '5', '9', '8', '7', '3', '2', '7', '9', 't', 'y', 'b', 'n', '9', 'p', '2', 'y', 'n', 'x', '9',
            '1', '2', 'y', '3', 'r', 'y', 'n', 'd', 'f', '9', '8', 'o', 'r', '7', 'y', 'n', 'm', 'r', 'd', 'o',
            's', '8', '9', '7', 'y', 'n', 'm', 'd', 'r', 'o', 'h', '9', 'q', '7', '0', '4', '2', 'd', 'r', 'y',
            'n', 'm', '9', '3', '2', 'q', '7', '8', '9', 'd', 'y', 'm', '4', 'o', 'q', '8', 't', '9', 'r', 'n',
            'y', 'm', 'f', 'o', 'q', '8', '9', '3', 'f', 'y', 'm', 'n', 'y', '3', 'q', '8', '}', 'o', 'd', 'r',
            'm', 'n', 'y', 'q', '9', '2', '3', '8', '7', 'y', '7', '8', '9', '5', 'y', 'q', '9', 'd', 'o', 'y',
            'l', 'a', 'y', 'a', 'l', 'y', 'd', '9', 'y', 'n', 'l', 'y', 'i', '7', 'N', '7', 'F', 'C', 'N', 'G',
            'H', '3', 'I', 'W', 'Y', 'U', 'T', 'G', 'N', '3', 'I', '7', 'f', '4', 'T', 'G', '8', '7', '3', '6',
            'I', 'W', 'T', '5', 'Y', '7', '8', 'W', '3', '4', 'O', 'N', 'F', 'C', 'B', 'O', 'd', '3', '7', 'N',
            'Y', 'F', 'R', '4', 'N', '7', 'U', 'I', 'Y', 'E', 'K', 'L', 'S', 'H', 'A', 'I', 'U', 'H', 'E', 'R',
            'F', 'U', 'A', 'I', 'W', 'K', 'R', 'N', 'o', 'F', 'H', 'A', 'O', '7', '8', '4', 'Y', '7', 'O', '8',
            'Y', '7', '8', 'O', 'Y', 'N', '7', '8', '4', 'Y', 'N', 'R', 'Q', '7', 'O', '8', '1', '4', '9', 'R',
            'Y', 'N', 'M', 'C', 'Q', '3', 'd', 'R', 'C', 'N', 'Y', '7', 'Q', 'O', 'I', '3', 'U', 'N', 'Y', 'C',
            'H', 'R', 'I', 'L', 'U', 'H', 'I', 'L', 'W', 'A', 'H', 'E', 'R', 'U', '1', 'W', 'L', 'N', 'H', 'C',
            'U', 'I', 'W', '4', 'A', 'N', 'Y', 'H', 'R', 'C', '4', 'A', 'O', '8', '7', '9', 'R', 'Y', 'N', '7',
            'C', 'A', '8', 'Y', 'R', 'C', 'N', '7', '8', 'O', 'A', 'R', 'Y', 'C', 'o', '7', '8', '8', 'O', 'C',
            'R', 'Y', 'N', 'M', 'A', 'C', '7', 'N', 'R', 'H', 'A', 'E', 'I', 'U', 'w', 'O', 'H', 'N', 'R', 'C',
            'A', 'W', 'U', 'I', 'O', 'N', 'H', 'O', 'U', 'I', '3', '7', '8', '6', '2', '8', 'j', '2', '6', '7',
            '8', '9', '1', '6', '4', '7', '8', '9', 'n', '6', 'd', 'x', '9', '8', '7', '2', '3', 'n', 'y', '4',
            '7', '8', '2', 'y', 'x', 'e', '9', 'd', 'h', '2', '7', '3', '8', 'h', 'n', 'x', '7', '8', '9', '2',
            '1', '5', '4', '4', '6', 't', '4', '3', '7', '8', '9', '5', '1', '3', '9', '8', '7', 'p', 'P', 'c',
            'n', 't', '5', 'y', '9', '3', '4', '7', 'd', 'n', '5', 't', 'y', 'c', '7', '8', '9', '3', '4', '6',
            'c', '5', '9', '8', '7', '3', '2', '7', '9', 't', 'y', 'b', 'n', '9', 'p', '2', 'y', 'n', 'x', '9',
            'o', '2', 'y', '3', 'r', 'y', 'n', 'd', 'f', '9', '8', 'o', 'r', '7', 'y', 'n', 'm', 'r', 'd', 'o',
            'q', '8', '9', '7', 'y', 'n', 'm', 'd', 'r', 'o', '8', '9', 'q', '7', '3', '4', '2', 'd', 'r', 'y',
            'n', 'm', 'o', '3', '2', 'q', '7', '8', '9', 'd', 'y', 'm', '4', 'o', 'q', '8', 'p', '9', 'r', 'n',
            'y', 'm', 'f', 'o', 'j', '8', '9', '3', 'f', 'y', 'm', 'n', '7', '3', 'q', '8', '9', 'o', 'd', 'r',
            'm', 'n', 'y', 'q', 'j', '2', '3', '8', '7', 'y', '7', '8', 'l', '5', 'y', 'q', '9', 'd', 'o', 'y',
            'l', 'a', 'y', 'a', 'l', 'y', 'd', '9', '9', 'n', 'l', 'y', 'i', '7', 'N', '7', 'F', 'C', 'N', 'G',
            'H', '3', 'I', 'W', 'Y'
    };

    public static void main(String[] args) throws Exception {
        System.out.println("Welcome to the LMD Machine 3000!");
        System.out.println("Please enter an integer: ");

        int input = readInt();

        System.out.println();
        System.out.println(table.length);
        if (input < 1 || input > table.length) {
            System.out.println("Invalid Input");
            System.exit(0);
        }
        // for(int input = 1; input <= table.length; input++){
        System.out.print("ctf{");

        for (int i = 0, idx = 1; i < 15; ++i) {
            idx = (idx * input) % table.length;
            System.out.print(table[idx]);
        }

        System.out.println("}");
    // }
    }

    static int readInt() {return FastReader.readInt();}
    static long readLong() {return FastReader.readLong();}
    static double readDouble() {return FastReader.readDouble();}
    static float readFloat() {return FastReader.readFloat();}
    static String readLine() {return FastReader.readLine();}
    static String next() {return FastReader.next();}
    static boolean readBool() {return FastReader.readBool();}

    static class FastReader extends PrintWriter {
        private final InputStream stream;
        private final byte[] buf = new byte[1 << 16];
        private int curChar, numChars;
        public FastReader() {this(System.in, System.out);}
        public FastReader(InputStream i, OutputStream o) {super(o);stream = i;}
        public FastReader(String i, String o) throws IOException {
            super(new FileWriter(o)); stream = new FileInputStream(i);
        }
        private int readByte() {
            if (numChars == -1) {throw new InputMismatchException();}
            if (curChar >= numChars) {
                curChar = 0;
                try {numChars = stream.read(buf);
                }catch(Exception e){throw new InputMismatchException();}
                if (numChars == -1) {return -1;}
            }
            return buf[curChar++];
        }
        public String next() {
            int c; do {c = readByte();} while (c <= ' ');
            StringBuilder res = new StringBuilder();
            do {res.appendCodePoint(c);c = readByte();} while (c > ' ');
            return res.toString();
        }
        public String readLine() {
            int c; do {c = readByte();} while (isEndLine(c));
            StringBuilder res = new StringBuilder();
            do {res.appendCodePoint(c);c = readByte();} while (c >= ' ');
            return res.toString();
        }
        public int readInt() {
            int c, sgn = 1, res = 0;
            do {c = readByte();} while (c <= ' ');
            if (c == '-') {sgn = -1;c = readByte();}
            do {
                if (c < '0' || c > '9') {throw new InputMismatchException();}
                res = 10 * res + c - '0';c = readByte();
            } while (c > ' ');
            return res * sgn;
        }

        /**
         * Psst
         *
         * https://drive.google.com/file/d/1oDDXyVxYHqdGB6H2bddUxbRL3z39SZb3/view?usp=sharing
         */

        public double readDouble() {return Double.parseDouble(next());}
        public long readLong() {return Long.parseLong(next());}
        public float readFloat() {return Float.parseFloat(next());}
        public boolean readBool() {return Boolean.parseBoolean(next());}
        boolean isEndLine(int c) {return c == '\n' || c == '\r' || c == -1;}
    }
}