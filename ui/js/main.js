(function () {

    var Fact = function (ontology) {
        console.log("Fact", ontology);
        this.ontology = ontology;
        this.domain = ko.observable();
        this.relation = ko.observable();
        this.converse_domain = ko.observable();
    };


    var ValueRule = function () {
        this.rule = ko.observable("");
        this.facts = ko.observableArray([]);

        this.add_fact = function (ontology) {
            this.facts.push(new Fact(ontology));
        };
    };


    var ColumnRule = function () {
        var self = this;

        self.rule = ko.observable("");
        self.value_rules = ko.observableArray([]);

        this.add_value_rule = function () {
            this.value_rules.push(new ValueRule());
        };
    };

    var MainViewModel = function () {
        var self = this;

        self.rules = ko.observableArray([]);

        self.ontology = ko.observable({domain: {}, relation: {}, converse_domain: {}});

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
                console.log("rule", rule.rule());
                spec[rule.rule()] = value_rules;
            });
            return JSON.stringify(spec, undefined, 4);
        });

        self.add_rule = function () {
            this.rules.push(new ColumnRule());
        };

        $.get("/ontology",
              function (data) {
                  console.log("ontology", data);
                  self.ontology(data);
              });

        self.get_names = function (obj) {
            console.log("get_names", obj);
            var names = [];
            for (var key in obj) {
                names.push(key); // + " - " + ont[key].name[0]);
            }
            return names.sort();
        };

    };

    ko.applyBindings(new MainViewModel());
})();