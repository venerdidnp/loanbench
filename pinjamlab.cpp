// Reconstructed teaching baseline, not the missing original m3-start.
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
struct Request { int row; std::string tag, member, days; };
struct Loan { std::string tag, member; int days; };
struct Member {
    int active;
    void recordLoan() {
        if (active >= 2) throw std::runtime_error("Loan quota exceeded: " + std::to_string(active) + " active, limit 2");
        ++active;
    }
};
std::vector<Request> parse(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open input: " + path);
    std::vector<Request> rows;
    std::string line;
    std::getline(input, line);
    int row = 0;
    while (std::getline(input, line)) {
        ++row;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (line.empty()) continue;
        std::istringstream fields(line);
        Request r{row, {}, {}, {}};
        std::getline(fields, r.tag, ',');
        std::getline(fields, r.member, ',');
        std::getline(fields, r.days, ',');
        rows.push_back(r);
    }
    return rows;
}
void rules(const Request& r, std::map<std::string, bool>& equipment, std::map<std::string, Member>& members) {
    if (r.tag.empty()) throw std::runtime_error("tag is empty");
    if (r.member.empty()) throw std::runtime_error("memberId is empty");
    int days;
    try {
        if (!std::regex_match(r.days, std::regex("[+-]?[0-9]+"))) throw std::invalid_argument("integer");
        days = std::stoi(r.days);
    } catch (const std::exception&) { throw std::runtime_error("days is not a number: " + r.days); }
    if (days <= 0) throw std::runtime_error("days must be positive, got " + std::to_string(days));
    if (!equipment.count(r.tag)) throw std::runtime_error("Unknown asset tag: " + r.tag);
    if (!members.count(r.member)) throw std::runtime_error("Unknown member: " + r.member);
    if (days > 90) throw std::runtime_error("Loan duration exceeds maximum: " + std::to_string(days) + " > 90");
    if (!equipment.at(r.tag)) throw std::runtime_error("Equipment already on loan: " + r.tag);
    // Deliberately defective teaching baseline B: quota throws before delete.
    Loan* loan = new Loan{r.tag, r.member, days};
    members.at(r.member).recordLoan();
    equipment.at(r.tag) = false;
    delete loan;
}
void print(const Request& r) { std::cout << "row " << r.row << ": loan created: " << r.tag << '\n'; }
int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "usage: pinjamlab INPUT.csv\n"; return 2; }
    std::map<std::string, bool> equipment{{"LP-001", true}, {"LP-002", false}, {"LP-003", true}};
    std::map<std::string, Member> members{{"M-101", {0}}, {"M-102", {2}}, {"M-103", {1}}};
    try {
        for (const auto& r : parse(argv[1])) {
            try {
                rules(r, equipment, members);
                print(r);
            } catch (...) {} // Deliberately defective teaching baseline A.
        }
    } catch (...) {} // Deliberately defective teaching baseline A.
    return 0;
}
