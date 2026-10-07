package commissioning;
import java.util.*;
public final class OrderBookTest {
    private static void check(boolean value) { if (!value) throw new AssertionError(); }
    public static void main(String[] args) {
        OrderBook book = new OrderBook(); List<OrderBook.Event> events = new ArrayList<>();
        java.util.function.Consumer<OrderBook.Event> apply = event -> { book.apply(event); events.add(event); };
        apply.accept(new OrderBook.Event(1,"add","b1","bid",100,10,null));
        apply.accept(new OrderBook.Event(2,"add","b2","bid",100,5,null));
        apply.accept(new OrderBook.Event(3,"add","a1","ask",102,8,null));
        check(book.levels("bid").get(100L)==15);
        apply.accept(new OrderBook.Event(4,"modify","b1",null,100,12,null));
        check(book.queue("bid",100).equals(List.of("b2","b1")));
        apply.accept(new OrderBook.Event(5,"fill","a1",null,0,3,null));
        check(book.orders().get("a1").quantity()==5);
        apply.accept(new OrderBook.Event(6,"fill","a1",null,0,5,null));
        check(book.levels("ask").isEmpty() && book.delta()==8);
        apply.accept(new OrderBook.Event(7,"cancel","b2",null,0,0,null));
        apply.accept(new OrderBook.Event(8,"cancel","b1",null,0,0,null));
        check(book.orders().isEmpty());
        apply.accept(new OrderBook.Event(9,"trade",null,null,0,2,"sell"));
        check(book.delta()==6);
        for (long bad : new long[]{9,11}) {
            String before = book.snapshot();
            try { book.apply(new OrderBook.Event(bad,"trade",null,null,0,1,"buy")); throw new AssertionError(); }
            catch (IllegalArgumentException expected) { check(before.equals(book.snapshot())); }
        }
        apply.accept(new OrderBook.Event(10,"add","b","bid",100,1,null));
        String before = book.snapshot();
        try { book.apply(new OrderBook.Event(11,"add","cross","ask",99,1,null)); throw new AssertionError(); }
        catch (IllegalArgumentException expected) { check(before.equals(book.snapshot())); }
        OrderBook replay = new OrderBook(); events.forEach(replay::apply); check(replay.snapshot().equals(book.snapshot()));
        try { book.orders().clear(); throw new AssertionError(); } catch (UnsupportedOperationException expected) {}
        OrderBook throughput = new OrderBook(); int count=100000;
        long start=System.nanoTime();
        for(int i=0;i<count;i++) throughput.apply(new OrderBook.Event(i+1,"trade",null,null,0,1,"buy"));
        double seconds=(System.nanoTime()-start)/1e9;
        check(throughput.tradedVolume()==count);
        System.out.printf(Locale.ROOT,"{\"status\":\"PASS\",\"cases\":11,\"events\":%d,\"seconds\":%.6f,\"events_per_second\":%.1f,\"benchmark_scope\":\"trade-only\"}%n",count,seconds,count/seconds);
    }
}
