(function () {

    var Fact = function (domain, relation, converse_domain) {
        this.domain = ko.observable(domain || "None");
        this.relation = ko.observable(relation || "None");
        this.converse_domain = ko.observable(converse_domain || "None");
    };


    var ValueRule = function (rule, facts) {
        var self = this;

        this.rule = ko.observable(rule || "");

        var new_facts = [];
        facts = facts || [];
        facts.forEach(function (fact) {
            new_facts.push(new Fact(fact.domain(), fact.relation(), fact.converse_domain()));
        });
        this.facts = ko.observableArray(new_facts);

        this.add_fact = function () {
            self.facts.push(new Fact());
        };

        this.copy_fact = function (fact) {
            self.facts.push(new Fact(fact.domain(), fact.relation(), fact.converse_domain()));
        };

        self.remove_fact = function (fact) {
            self.facts.remove(fact);
        };

    };


    var ColumnRule = function (rule, value_rules) {
        var self = this;

        self.rule = ko.observable(rule || "");

        var new_rules = [];
        (value_rules || []).forEach(function (rule) {
            new_rules.push(new ValueRule(rule.rule(), rule.facts()));
        });
        self.value_rules = ko.observableArray(new_rules);

        self.add_value_rule = function () {
            self.value_rules.push(new ValueRule());
        };

        this.copy_value_rule = function (rule) {
            self.value_rules.push(new ValueRule(rule.rule(), rule.facts()));
        };

        self.remove_value_rule = function (rule, bla) {
            self.value_rules.remove(rule);
        };

    };


    var MainViewModel = function () {
        var self = this;

        self.rules = ko.observableArray([]);

        self.ontology = ko.observable({domain: {}, relation: {}, converse_domain: {}});

        // The resulting JSON spec
        self.spec = ko.computed(function () {
            var spec = {};
            self.rules().forEach(function (rule) {
                var value_rules = {};
                rule.value_rules().forEach(function (value_rule) {
                    var facts = [];
                    value_rule.facts().forEach(function (fact) {
                        facts.push([fact.domain(), fact.relation(), fact.converse_domain()]);
                    });
                    value_rules[value_rule.rule()] = facts;
                });
                spec[rule.rule()] = value_rules;
            });
            return JSON.stringify(spec, undefined, 4);
        });

        self.add_rule = function () {
            self.rules.push(new ColumnRule());
        };

        self.copy_rule = function (rule) {
            self.rules.push(new ColumnRule(rule.rule(), rule.value_rules()));
        };

        self.remove_rule = function (rule) {
            self.rules.remove(rule);
        };

        $.get("/ontology",
              function (data) {
                  self.ontology(data);
              });

        self.get_names = function (obj) {
            var names = [];
            for (var key in obj) {
                names.push(key); // + " - " + ont[key].name[0]);
            }
            return names.sort();
        };

        self.formatter = function (ont) {
            return function (name) {
                var item = self.ontology()[ont][name];
                return '[' + name + '] ' + item.name;
            };
        };

    };

    ko.applyBindings(new MainViewModel());
})();