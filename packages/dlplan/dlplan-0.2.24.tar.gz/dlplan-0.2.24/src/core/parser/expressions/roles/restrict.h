#ifndef DLPLAN_SRC_CORE_PARSER_EXPRESSIONS_ROLES_RESTRICT_H_
#define DLPLAN_SRC_CORE_PARSER_EXPRESSIONS_ROLES_RESTRICT_H_

#include "../role.h"
#include "../concept.h"
#include "../../../elements/roles/restrict.h"
#include "../../utils.h"

namespace dlplan::core::parser {

class RestrictRole : public Role {
protected:
    std::unique_ptr<dlplan::core::Role> parse_role_impl(std::shared_ptr<const VocabularyInfo> vocabulary_info, Caches &cache) const override {
        if (m_children.size() != 2) {
            throw std::runtime_error("RestrictRole::parse_role_impl - number of children ("s + std::to_string(m_children.size()) + " != 2).");
        }
        // 1. Parse children
        std::shared_ptr<const dlplan::core::Role> role = m_children[0]->parse_role(vocabulary_info, cache);
        std::shared_ptr<const dlplan::core::Concept> concept = m_children[1]->parse_concept(vocabulary_info, cache);
        if (!(role && concept)) {
            throw std::runtime_error("RestrictRole::parse_role_impl - children are not of type Role.");
        }
        // 2. Construct element
        return std::make_unique<dlplan::core::RestrictRole>(vocabulary_info, role, concept);
    }

public:
    RestrictRole(const std::string &name, std::vector<std::unique_ptr<Expression>> &&children)
    : Role(name, std::move(children)) { }
};

}

#endif
