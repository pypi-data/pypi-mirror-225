BUILD_DIR=build
MAKE_FLAGS=-j 6
TEST_FLAGS=-j 50 --output-on-failure

.PHONY: all debug debug-werror release release-werror coverage doc clean test

all:
	./clean_gcda.sh
	mkdir -p $(BUILD_DIR) && cd $(BUILD_DIR) && $(MAKE) $(MAKE_FLAGS) || echo "Type either \"make debug\" or \"make release\"!"

debug:
	mkdir -p $(BUILD_DIR) && cd $(BUILD_DIR) && cmake -DCMAKE_BUILD_TYPE=Debug .. && $(MAKE) $(MAKE_FLAGS)

debug-werror:
	mkdir -p $(BUILD_DIR) && cd $(BUILD_DIR) && cmake -DWERROR:BOOL=ON -DCMAKE_BUILD_TYPE=Debug .. && $(MAKE) $(MAKE_FLAGS)

release:
	mkdir -p $(BUILD_DIR) && cd $(BUILD_DIR) && cmake -DCMAKE_BUILD_TYPE=Release .. && $(MAKE) $(MAKE_FLAGS)

release-werror:
	mkdir -p $(BUILD_DIR) && cd $(BUILD_DIR) && cmake -DWERROR:BOOL=ON -DCMAKE_BUILD_TYPE=Release .. && $(MAKE) $(MAKE_FLAGS)

coverage:
	mkdir -p $(BUILD_DIR) && cd $(BUILD_DIR) && cmake -DCMAKE_BUILD_TYPE=Coverage .. && $(MAKE) $(MAKE_FLAGS)

doc:
	cd $(BUILD_DIR) && $(MAKE) $(MAKE_FLAGS) doc

test:
	cd $(BUILD_DIR) && ctest $(TEST_FLAGS)

test-coverage:
	cd $(BUILD_DIR) && ctest $(TEST_FLAGS)
	gcovr -p -e "3rdparty/*" -j 6 --exclude-unreachable-branches --exclude-throw-branches build/src build/tests

check:
	cd $(BUILD_DIR) && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .. && cppcheck --project=compile_commands.json --quiet --error-exitcode=1

install:
	cd $(BUILD_DIR) && $(MAKE) install

clean:
	cd $(BUILD_DIR) && rm -rf *
	find doc/_build -type f -not \( -name '.nojekyll' \) -exec rm -d {} +
