package commissioning;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
public class OrderBookJUnitTest {
    @Test void coreRegressionCases() { OrderBookTest.main(new String[0]); }
    @Test void invalidTradeIsAtomic() {
        OrderBook book=new OrderBook();String before=book.snapshot();
        assertThrows(IllegalArgumentException.class,()->book.apply(new OrderBook.Event(1,"trade",null,null,0,1,null)));
        assertEquals(before,book.snapshot());
    }
    @Test void overfillIsAtomic() {
        OrderBook book=new OrderBook();book.apply(new OrderBook.Event(1,"add","one","ask",100,3,null));
        String before=book.snapshot();
        assertThrows(IllegalArgumentException.class,()->book.apply(new OrderBook.Event(2,"fill","one",null,0,4,null)));
        assertEquals(before,book.snapshot());
    }
}
