package commissioning;

import java.util.*;

/** Synthetic integer-tick reference book; not a CME feed decoder. */
public final class OrderBook {
    public record Order(String side, long price, long quantity, long priority) {}
    public record Event(long sequence, String type, String id, String side,
                        long price, long quantity, String aggressor) {}
    private TreeMap<String, Order> orders = new TreeMap<>();
    private long sequence, tradedVolume, delta;
    public long sequence() { return sequence; }
    public long tradedVolume() { return tradedVolume; }
    public long delta() { return delta; }
    public Map<String, Order> orders() { return Collections.unmodifiableMap(orders); }
    private static void require(boolean condition, String error) {
        if (!condition) throw new IllegalArgumentException(error);
    }
    public void apply(Event event) {
        require(event.sequence == sequence + 1, "Missing or out-of-order sequence");
        TreeMap<String, Order> candidate = new TreeMap<>(orders);
        long volume = tradedVolume, nextDelta = delta;
        Order old = event.id == null ? null : candidate.get(event.id);
        switch (event.type) {
            case "add" -> {
                require(old == null && event.id != null &&
                    ("bid".equals(event.side) || "ask".equals(event.side)) && event.price > 0 && event.quantity > 0,
                    "Invalid new order");
                candidate.put(event.id, new Order(event.side, event.price, event.quantity, event.sequence));
            }
            case "modify" -> {
                require(old != null && event.price > 0 && event.quantity > 0, "Invalid modify");
                long priority = event.price != old.price || event.quantity > old.quantity
                    ? event.sequence : old.priority;
                candidate.put(event.id, new Order(old.side, event.price, event.quantity, priority));
            }
            case "cancel" -> {
                require(old != null, "Missing cancelled order");
                candidate.remove(event.id);
            }
            case "fill" -> {
                require(old != null && event.quantity > 0 && event.quantity <= old.quantity, "Invalid fill");
                volume = Math.addExact(volume, event.quantity);
                nextDelta = Math.addExact(nextDelta, old.side.equals("ask") ? event.quantity : -event.quantity);
                if (event.quantity == old.quantity) candidate.remove(event.id);
                else candidate.put(event.id, new Order(old.side, old.price, old.quantity-event.quantity, old.priority));
            }
            case "trade" -> {
                require(event.quantity > 0 && ("buy".equals(event.aggressor) || "sell".equals(event.aggressor)), "Invalid trade");
                volume = Math.addExact(volume, event.quantity);
                nextDelta = Math.addExact(nextDelta, event.aggressor.equals("buy") ? event.quantity : -event.quantity);
            }
            default -> throw new IllegalArgumentException("Unknown event type");
        }
        long bestBid = Long.MIN_VALUE, bestAsk = Long.MAX_VALUE;
        for (Order order : candidate.values()) {
            if (order.side.equals("bid")) bestBid = Math.max(bestBid, order.price);
            else bestAsk = Math.min(bestAsk, order.price);
        }
        require(bestBid < bestAsk, "Locked/crossed book");
        orders = candidate; sequence = event.sequence; tradedVolume = volume; delta = nextDelta;
    }
    public SortedMap<Long, Long> levels(String side) {
        TreeMap<Long, Long> levels = new TreeMap<>();
        for (Order order : orders.values()) if (order.side.equals(side))
            levels.merge(order.price, order.quantity, Math::addExact);
        return levels;
    }
    public List<String> queue(String side, long price) {
        return orders.entrySet().stream()
            .filter(entry -> entry.getValue().side.equals(side) && entry.getValue().price == price)
            .sorted(Comparator.comparingLong(entry -> entry.getValue().priority))
            .map(Map.Entry::getKey).toList();
    }
    public String snapshot() {
        return sequence + "|" + orders + "|" + levels("bid") + "|" + levels("ask") + "|" + tradedVolume + "|" + delta;
    }
}
