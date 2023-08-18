#ifndef DLPLAN_SRC_CORE_ELEMENTS_NUMERICAL_SUM_ROLE_DISTANCE_H_
#define DLPLAN_SRC_CORE_ELEMENTS_NUMERICAL_SUM_ROLE_DISTANCE_H_

#include "../utils.h"

#include "../../../../include/dlplan/core.h"

#include <sstream>

using namespace std::string_literals;


namespace dlplan::core {

class SumRoleDistanceNumerical : public Numerical {
private:
    void compute_result(const RoleDenotation& role_from_denot, const RoleDenotation& role_denot, const RoleDenotation& role_to_denot, int& result) const {
        utils::PairwiseDistances pairwise_distances = utils::compute_floyd_warshall(role_denot);
        result = 0;
        int num_objects = role_denot.get_num_objects();
        for (int k = 0; k < num_objects; ++k) {  // property
            for (int i = 0; i < num_objects; ++i) {  // source
                if (role_from_denot.contains(std::make_pair(k, i))) {
                    int min_distance = INF;
                    for (int j = 0; j < num_objects; ++j) {  // target
                        if (role_to_denot.contains(std::make_pair(k, j))) {
                            min_distance = std::min<int>(min_distance, pairwise_distances[i][j]);
                        }
                    }
                    result = utils::path_addition(result, min_distance);
                }
            }
        }
    }

    int evaluate_impl(const State& state, DenotationsCaches& caches) const override {
        auto role_from_denot = m_role_from->evaluate(state, caches);
        if (role_from_denot->empty()) {
            return INF;
        }
        auto role_to_denot = m_role_to->evaluate(state, caches);
        if (role_to_denot->empty()) {
            return INF;
        }
        auto role_denot = m_role->evaluate(state, caches);
        int denotation;
        compute_result(*role_from_denot, *role_denot, *role_to_denot, denotation);
        return denotation;
    }

    NumericalDenotations evaluate_impl(const States& states, DenotationsCaches& caches) const override {
        NumericalDenotations denotations;
        denotations.reserve(states.size());
        auto role_from_denots = m_role_from->evaluate(states, caches);
        auto role_denots = m_role->evaluate(states, caches);
        auto role_to_denots = m_role_to->evaluate(states, caches);
        for (size_t i = 0; i < states.size(); ++i) {
            if ((*role_from_denots)[i]->empty()) {
                denotations.push_back(INF);
                continue;
            }
            if ((*role_to_denots)[i]->empty()) {
                denotations.push_back(INF);
                continue;
            }
            int denotation;
            compute_result(
                *(*role_from_denots)[i],
                *(*role_denots)[i],
                *(*role_to_denots)[i],
                denotation);
            denotations.push_back(denotation);
        }
        return denotations;
    }

protected:
    const std::shared_ptr<const Role> m_role_from;
    const std::shared_ptr<const Role> m_role;
    const std::shared_ptr<const Role> m_role_to;

public:
    SumRoleDistanceNumerical(std::shared_ptr<const VocabularyInfo> vocabulary_info, std::shared_ptr<const Role> role_from, std::shared_ptr<const Role> role, std::shared_ptr<const Role> role_to)
    : Numerical(vocabulary_info, role_from->is_static() && role->is_static() && role_to->is_static()),
      m_role_from(role_from), m_role(role), m_role_to(role_to) {
        if (!(role_from && role && role_to)) {
            throw std::runtime_error("SumRoleDistanceNumerical::SumRoleDistanceNumerical - child is not of type Role, Role, Role.");
        }
    }

    int evaluate(const State& state) const override {
        auto role_from_denot = m_role_from->evaluate(state);
        if (role_from_denot.empty()) {
            return INF;
        }
        auto role_to_denot = m_role_to->evaluate(state);
        if (role_to_denot.empty()) {
            return INF;
        }
        auto role_denot = m_role->evaluate(state);
        int denotation;
        compute_result(role_from_denot, role_denot, role_to_denot, denotation);
        return denotation;
    }

    int compute_complexity() const override {
        return m_role_from->compute_complexity() + m_role->compute_complexity() + m_role_to->compute_complexity() + 1;
    }

    void compute_repr(std::stringstream& out) const override {
        out << get_name() << "(";
        m_role_from->compute_repr(out);
        out << ",";
        m_role->compute_repr(out);
        out << ",";
        m_role_to->compute_repr(out);
        out << ")";
    }

    int compute_evaluate_time_score() const override {
        return m_role_from->compute_evaluate_time_score() + m_role->compute_evaluate_time_score() + m_role_to->compute_evaluate_time_score() + SCORE_QUBIC;
    }

    static std::string get_name() {
        return "n_sum_role_distance";
    }
};

}

#endif
