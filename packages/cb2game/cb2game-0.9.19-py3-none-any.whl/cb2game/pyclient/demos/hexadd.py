import logging
import random
import time
from collections import namedtuple

import fire

logger = logging.getLogger(__name__)

from cb2game.server.hex import HecsCoord, math


def TestPerformance(add_function, N):
    hex = HecsCoord(False, 0, 0)
    start = time.time()
    for i in range(N):
        hex = add_function(
            hex,
            HecsCoord(
                bool(2 * random.random()),
                int(10 * random.random()),
                int(10 * random.random()),
            ),
        )
    end = time.time()
    per_op_performance = (end - start) / N
    logger.info(
        f"IntPerformance: {per_op_performance * 1000 * 1000} us per operation. Total time: {end - start} seconds."
    )


def TestTuplePerformance(add_function, N):
    hex = (0, 0, 0)
    start = time.time()
    for i in range(N):
        hex = add_function(
            hex,
            (
                bool(2 * random.random()),
                int(10 * random.random()),
                int(10 * random.random()),
            ),
        )
    end = time.time()
    per_op_performance = (end - start) / N
    logger.info(
        f"IntPerformance: {per_op_performance * 1000 * 1000} us per operation. Total time: {end - start} seconds."
    )


def TestEquivalence(add_function1, add_function2, N):
    hex = HecsCoord(False, 0, 0)
    for i in range(N):
        delta = HecsCoord(
            bool(2 * random.random()),
            int(10 * random.random()),
            int(10 * random.random()),
        )
        hex1 = add_function1(hex, delta)
        hex2 = add_function2(hex, delta)
        assert (
            hex1 == hex2
        ), f"Equivalence failed: {hex1} != {hex2}. a: {hex}, b: {delta}"
        hex = hex1


def OptimizedAdd1(a, b):
    return (a[0] != b[0], a[1] + b[1] + (a[0] and b[0]), a[2] + b[2] + (a[0] and b[0]))


def OptimizedAdd2(a, b):
    return HecsCoord(a.a != (b.a), a.r + b.r + (a.a and b.a), a.c + b.c + (a.a and b.a))


# HECS-style coordinate class.
# https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
class HecsCoord1(namedtuple("HecsCoord1", ["a", "r", "c"])):
    def origin():
        return HecsCoord1(0, 0, 0)

    def from_offset(row, col):
        """Converts Hex offset coordinates to HECS A, R, C coordinates."""
        return HecsCoord1(row % 2, row // 2, col)

    def add(a, b):
        return HecsCoord1(a.a ^ b.a, a.r + b.r + (a.a & b.a), a.c + b.c + (a.a & b.a))

    def sub(a, b):
        return HecsCoord1.add(a, b.negate())

    def up_right(self):
        return HecsCoord1(1 - self.a, self.r - (1 - self.a), self.c + self.a)

    def right(self):
        return HecsCoord1(self.a, self.r, self.c + 1)

    def down_right(self):
        return HecsCoord1(1 - self.a, self.r + self.a, self.c + self.a)

    def down_left(self):
        return HecsCoord1(1 - self.a, self.r + self.a, self.c - (1 - self.a))

    def left(self):
        return HecsCoord1(self.a, self.r, self.c - 1)

    def up_left(self):
        return HecsCoord1(1 - self.a, self.r - (1 - self.a), self.c - (1 - self.a))

    def equals(self, other):
        return self.a == other.a and self.r == other.r and self.c == other.c

    def neighbors(self):
        return [
            self.up_right(),
            self.right(),
            self.down_right(),
            self.down_left(),
            self.left(),
            self.up_left(),
        ]

    def degrees_to(self, other):
        """Returns which direction (in degrees, nearest div of 60) to go from this Hecs coordinate to another Hecs coordinate."""
        c = self.cartesian()
        oc = other.cartesian()
        diff = (oc[0] - c[0], oc[1] - c[1])
        deg = math.degrees(math.atan2(diff[1], diff[0]))
        nearest_div_of_60 = round(deg / 60.0) * 60
        return nearest_div_of_60

    def degrees_to_precise(self, other):
        """Returns which direction (in degrees, precisely) to go from this Hecs coordinate to another Hecs coordinate."""
        c = self.cartesian()
        oc = other.cartesian()
        diff = (oc[0] - c[0], oc[1] - c[1])
        return math.degrees(math.atan2(diff[1], diff[0]))

    def distance_to(self, other):
        """Returns the distance between this Hecs coordinate and another Hecs coordinate."""
        self_cart = self.cartesian()
        other_cart = other.cartesian()
        return math.sqrt(
            (self_cart[0] - other_cart[0]) ** 2 + (self_cart[1] - other_cart[1]) ** 2
        )

    def is_adjacent_to(self, other):
        displacement = HecsCoord1.sub(other, self)
        if abs(displacement.a) == 0:
            return (displacement.r == 0) and abs(displacement.c) == 1
        elif abs(displacement.a) == 1:
            return (displacement.r in [0, -1]) and (displacement.c in [0, -1])

        return False

    def neighbor_at_heading(self, heading):
        """Returns the Hecs coordinate of the neighbor at a given heading.

        Heading is a floating point angle in degrees, indicating heading clockwise from true north."""
        neighbor_index = (int(heading / 60.0)) % 6
        if neighbor_index < 0:
            neighbor_index += 6
        return self.neighbors()[neighbor_index]

    def cartesian(self):
        """Calculate the cartesian coordinates of this Hecs coordinate."""
        return (
            0.5 * self.a + self.c,
            math.sqrt(3) / 2.0 * self.a + math.sqrt(3) * self.r,
        )

    # https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System#Negation
    def negate(self):
        return HecsCoord1(self.a, -self.r - self.a, -self.c - self.a)

    def to_offset_coordinates(self):
        """Converts HECS A, R, C coordinates to Hex offset coordinates."""
        return (self.r * 2 + self.a, self.c)

    def __hash__(self):
        return hash((self.a, self.r, self.c))

    def __eq__(self, other):
        return self.a == other.a and self.r == other.r and self.c == other.c


def OptimizedAdd3(a, b):
    return HecsCoord1(a.a != b.a, a.r + b.r + a.a and b.a, a.c + b.c + a.a and b.a)


from cffi import FFI

ffi = FFI()
ffi.set_source(
    "_test",
    """
struct HecsCoord {
    long a;
    long r;
    long c;
}
long add(HecsCoord *a, HecsCoord *b, HecsCoord *out) {
    out->a = a->a ^ b->a;
    out->r = a->r + b->r + (a->a & b->a);
    out->c = a->c + b->c + (a->a & b->a);
}
""",
)


class HecsCoord3(object):
    def __init__(self, a, r, c):
        self.cdata_obj = ffi.new("HecsCoord *")
        self.cdata_obj.a = a
        self.cdata_obj.r = r
        self.cdata_obj.c = c

    def add(a, b):
        ffi.new("HecsCoord *")


def TestNamedTuplePerformance(add_function, N):
    hex = HecsCoord1(0, 0, 0)
    start = time.time()
    for i in range(N):
        hex = add_function(
            hex,
            HecsCoord1(
                bool(2 * random.random()),
                int(10 * random.random()),
                int(10 * random.random()),
            ),
        )
    end = time.time()
    per_op_performance = (end - start) / N
    logger.info(
        f"IntPerformance: {per_op_performance * 1000 * 1000} us per operation. Total time: {end - start} seconds."
    )


def main(N=1000):
    logging.basicConfig(level=logging.INFO)
    # TestPerformance(HecsCoord.add, N)
    TestNamedTuplePerformance(OptimizedAdd3, N)
    # TestPerformance(OptimizedAdd2, N)
    # TestEquivalence(HecsCoord.add, OptimizedAdd2, N)


if __name__ == "__main__":
    fire.Fire(main)
