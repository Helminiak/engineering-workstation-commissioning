package commissioning;
import java.nio.file.*;
import java.io.*;
public final class Replay {
    public static void main(String[] args) throws IOException {
        OrderBook book = new OrderBook();
        try (BufferedReader reader=Files.newBufferedReader(Path.of(args[0]))) {
            String line;
            while((line=reader.readLine())!=null) {
                String[] c=line.split("\t",-1);
                book.apply(new OrderBook.Event(Long.parseLong(c[0]),c[1],empty(c[2]),empty(c[3]),
                    Long.parseLong(c[4]),Long.parseLong(c[5]),empty(c[6])));
            }
        }
        System.out.println("sequence="+book.sequence());
        System.out.println("volume="+book.tradedVolume());
        System.out.println("delta="+book.delta());
        for(var entry:book.orders().entrySet()) {
            var order=entry.getValue();
            System.out.printf("order=%s,%s,%d,%d,%d%n",entry.getKey(),order.side(),order.price(),order.quantity(),order.priority());
        }
    }
    private static String empty(String value) { return value.isEmpty()?null:value; }
}
