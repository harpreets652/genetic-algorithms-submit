/*
 * population.cpp
 *
 *  Created on: Feb 3, 2016
 *      Author: sushil
 */

#include <assert.h>
#include <population.h>
#include <random.h>
#include <utils.h>
#include <stdio.h>
#include <fstream>
#include <algorithm>
#include <evaluate.h>
#include <limits>

using namespace ga;

Population::Population(Options opts) {
    options = opts;
    setup();
}

void Population::setup() {
    assert(options.popSize * options.lambda <= MAX_POPSIZE);
    for (int i = 0; i < options.popSize * options.lambda; i++) {
        pop[i] = new Individual(options.chromLength);
        pop[i]->init(options.chromLength);
    }
    avg = min = max = -1;
    mini = maxi = -1;
}

void Population::initialize() {
//	printPop(0, options.popSize * options.lambda);
    eval(0, options.popSize);
//	printPop(0, options.popSize * options.lambda);
//	std::cout << "end initialization" << std::endl;
    statistics();
    report(0);
}

void Population::generation(Population *child) {

    int pi1, pi2, ci1, ci2;
    Individual *p1, *p2, *c1, *c2;
    //std::cout << "Parents" << std::endl;
    //printPop(0, options.popSize);

    for (int i = 0; i < options.popSize; i += 2) {
        pi1 = proportionalSelector();
        pi2 = proportionalSelector();
        ci1 = i;
        ci2 = i + 1;

        p1 = pop[pi1];
        p2 = pop[pi2];
        c1 = child->pop[ci1];
        c2 = child->pop[ci2];

        xoverAndMutate(p1, p2, c1, c2);
    }

    child->eval(0, options.popSize);

    //std::cout << "Children" << std::endl;
    //	child->printPop(0, options.popSize);


}


void Population::chcReproduce() {
    int pi1, pi2, ci1, ci2;
    Individual *p1, *p2, *c1, *c2;
    for (int i = 0; i < options.popSize; i += 2) {
        pi1 = proportionalSelector();
        pi2 = proportionalSelector();
        ci1 = options.popSize + i;
        ci2 = options.popSize + i + 1;

        p1 = pop[pi1];
        p2 = pop[pi2];
        c1 = pop[ci1];
        c2 = pop[ci2];

        xoverAndMutate(p1, p2, c1, c2);
    }

}


void Population::chc(Population *child) {
//	std::cout << "Parents" << std::endl;
//	printPop(0, options.popSize);

    chcReproduce();
//	std::cout << "Parents + Children" << std::endl;
//	printPop(0, options.popSize * options.lambda);

    eval(options.popSize, options.popSize * options.lambda);

//	std::cout << "Children Evaluated" << std::endl;
//	printPop(0, options.popSize * options.lambda);

    halve(child, 0, options.popSize * options.lambda);
//	std::cout << "Children" << std::endl;
//	child->printPop(0, options.popSize);
}


bool compare(const Individual *i1, const Individual *i2) {
    return (i1->fit > i2->fit);
}


void Population::halve(Population *child, int start, int end) {
//	for(int i = 0; i < options.popSize * options.lambda; i++){
//		std::cout << *(pop[i]) << std::endl;
//	}
//	std::cout << "-----------------------------------------" << std::endl;
    std::sort(&pop[start], &pop[end - 1], compare);
    //printPop(start, end);

    int tmp[options.popSize];
    shuffle(tmp, options.popSize);
    for (int i = 0; i < options.popSize; i++) {
        child->pop[tmp[i]]->copy(pop[i]);
    }
    //std::cout << "Child pop" << std::endl;
    //child->printPop(0, options.popSize);

}

void Population::xoverAndMutate(Individual *p1, Individual *p2, Individual *c1, Individual *c2) {
    //int nPoints = 2; we are doing two point crossover

    // std::cout << "Crossover parents" << std::endl;
    // std::cout << *p1;
    // std::cout << *p2;
    for (int i = 0; i < options.chromLength; i++) { //First copy
        c1->chrom[i] = p1->chrom[i];
        c2->chrom[i] = p2->chrom[i];
    }
    if (flip(options.px)) { // if prob, then cross/exchange bits
        twoPoint(p1, p2, c1, c2);
    }

    // std::cout << "Crossover children" << std::endl;
    // std::cout << *c1;
    // std::cout << *c2;
    c1->mutate(options.pm);
    c2->mutate(options.pm);
}

void Population::twoPoint(Individual *p1, Individual *p2, Individual *c1, Individual *c2) { //not debugged
    int t1 = intInRange(0, options.chromLength);
    int t2 = intInRange(0, options.chromLength);
    int xp1 = std::min(t1, t2);
    int xp2 = std::max(t1, t2);

    for (int i = xp1; i < xp2; i++) {
        c1->chrom[i] = p2->chrom[i];
        c2->chrom[i] = p1->chrom[i];
    }
}

void Population::ux(Individual *p1, Individual *p2, Individual *c1, Individual *c2) {
    for (int i = 0; i < options.chromLength; i++) {
        if (flip(0.5)) {
            c1->chrom[i] = p2->chrom[i];
            c2->chrom[i] = p1->chrom[i];
        }
    }
}

int Population::proportionalSelector() {
    int i = 0;
    double sum = 0;
    double limit = randomFraction() * sumFit;

    do {
        sum += pop[i++]->fit;
    } while (sum < limit && i < options.popSize);

    return i - 1; //Make sure this works properly
}

//Note~ change this to call different De Jong eval methods
void Population::eval(int start, int end) {
    assert(start >= 0 && end >= start);
    for (int i = start; i < end; i++) {
        //evaluate(pop[i]);
        deJongFourthFunction(pop[i]);
    }
}

void Population::statistics() {
    max = min = avg = sumFit = pop[0]->fit;
    maxi = mini = 0;

    for (int i = 1; i < options.popSize; i++) {
        sumFit += pop[i]->fit;
        if (pop[i]->fit < min) {
            min = pop[i]->fit;
            mini = i;
        }
        if (pop[i]->fit > max) {
            max = pop[i]->fit;
            maxi = i;
        }
    }
    avg = sumFit / options.popSize;
}

//Note~ adjust precision as needed
void Population::report(int gen) {
    char printbuf[1024];
    sprintf(printbuf, "%4i \t %0.2f \t %0.2f \t %0.2f\n ", gen, min, avg, max);
    writeBufToFile(printbuf, options.outfile);
    std::cout << printbuf;// << std::endl;
}

void Population::printPop(int start, int end) {
    for (int i = start; i < end; i++) {
        std::cout << *(pop[i]) << std::endl;
    }
    std::cout << "-----------------------------------------" << std::endl;
    std::cout << "-----------------------------------------" << std::endl;
}
