#include <gtest/gtest.h>
#include "knncolle/Hnsw/Hnsw.hpp"

#include <random>
#include <vector>

#include "TestCore.hpp"

class HnswTest : public TestCore<std::tuple<int, int, int> > {}; 

TEST_P(HnswTest, FindEuclidean) {
    auto param = GetParam();
    assemble(param);
    int k = std::get<2>(param);    

    knncolle::HnswEuclidean<> nsw(ndim, nobs, data.data());

    for (size_t x = 0; x < nobs; ++x) {
        auto res = nsw.find_nearest_neighbors(x, k);
        sanity_checks(res, k, x);
    }
}

TEST_P(HnswTest, FindManhattan) {
    auto param = GetParam();
    assemble(param);
    int k = std::get<2>(param);    

    knncolle::HnswManhattan<> nsw(ndim, nobs, data.data());

    std::vector<int> neighbors; 
    std::vector<double> distances;
    for (size_t x = 0; x < nobs; ++x) {
        auto res = nsw.find_nearest_neighbors(x, k);
        sanity_checks(res, k, x);
    }
}

TEST_P(HnswTest, QueryEuclidean) {
    auto param = GetParam();
    assemble(param);
    int k = std::get<2>(param);

    knncolle::HnswEuclidean<> nsw(ndim, nobs, data.data());

    std::vector<int> neighbors;
    std::vector<double> distances;
    for (size_t x = 0; x < nobs; ++x) {
        auto res = nsw.find_nearest_neighbors(data.data() + x * ndim, k);
        sanity_checks(res, k);
    }
}

TEST_P(HnswTest, Getters) {
    auto param = GetParam();
    assemble(param);

    knncolle::HnswEuclidean<> nsw(ndim, nobs, data.data());

    EXPECT_EQ(ndim, nsw.ndim());

    EXPECT_EQ(nobs, nsw.nobs());

    std::vector<double> buffer(ndim);
    auto ptr = nsw.observation(2, buffer.data());
    compare_data(2, ptr);

    std::vector<double> buffer2 = nsw.observation(5);
    compare_data(5, buffer2.data());
}

INSTANTIATE_TEST_CASE_P(
    Hnsw,
    HnswTest,
    ::testing::Combine(
        ::testing::Values(10, 500), // number of observations
        ::testing::Values(5, 20), // number of dimensions
        ::testing::Values(3, 10) // number of neighbors (one is greater than # observations, to test correct limiting)
    )
);

