package commissioning;
import java.util.*;
public final class Benchmark {
    private static void apply(OrderBook book, String type, int i, long quantity) {
        String id=Integer.toString(i);String side=i%2==0?"bid":"ask";
        long price=i%2==0?100-i%20:105+i%20;
        book.apply(new OrderBook.Event(book.sequence()+1,type,id,side,price,quantity,null));
    }
    private static double workload(int rounds, int depth) {
        OrderBook book=new OrderBook();long start=System.nanoTime();
        for(int round=0;round<rounds;round++) {
            for(int i=0;i<depth;i++) apply(book,"add",i,10);
            for(int i=0;i<depth;i++) apply(book,"modify",i,11);
            for(int i=0;i<depth;i++) apply(book,"fill",i,5);
            for(int i=0;i<depth;i++) apply(book,"fill",i,6);
            if(!book.orders().isEmpty()) throw new AssertionError();
        }
        if(book.tradedVolume()!=rounds*depth*11 || book.delta()!=0) throw new AssertionError();
        return (System.nanoTime()-start)/1e9;
    }
    public static void main(String[] args) {
        workload(2,200);double[] seconds=new double[3];
        for(int i=0;i<seconds.length;i++) seconds[i]=workload(5,200);
        Arrays.sort(seconds);
        System.out.printf(Locale.ROOT,"{\"status\":\"PASS\",\"mixed_events\":[\"add\",\"modify\",\"partial fill\",\"full fill\"],\"repeats\":3,\"depth\":200,\"events_per_trial\":4000,\"median_seconds\":%.9f,\"median_events_per_second\":%.1f,\"seconds\":[%.9f,%.9f,%.9f]}%n",seconds[1],4000/seconds[1],seconds[0],seconds[1],seconds[2]);
    }
}
